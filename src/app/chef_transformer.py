from transformers import FlaxAutoModelForSeq2SeqLM
from transformers import AutoTokenizer

import logging

logger = logging.getLogger(__name__)


class Chef:
    def __init__(self) -> None:
        self.MODEL_NAME_OR_PATH = "flax-community/t5-recipe-generation"
        self.tokenizer = AutoTokenizer.from_pretrained(
            self.MODEL_NAME_OR_PATH, use_fast=True
        )
        self.model = FlaxAutoModelForSeq2SeqLM.from_pretrained(self.MODEL_NAME_OR_PATH)

        self.special_tokens = self.tokenizer.all_special_tokens
        self.tokens_map = {"<sep>": "--", "<section>": "\n"}

        self.prefix = "items: "
        # generation_kwargs = {
        #     "max_length": 512,
        #     "min_length": 64,
        #     "no_repeat_ngram_size": 3,
        #     "early_stopping": True,
        #     "num_beams": 5,
        #     "length_penalty": 1.5,
        # }
        self.generation_kwargs = {
            "max_length": 512,
            "min_length": 64,
            "no_repeat_ngram_size": 3,
            "do_sample": True,
            "top_k": 60,
            "top_p": 0.95,
        }

    def skip_special_tokens(self, text, special_tokens):
        for token in special_tokens:
            text = text.replace(token, "")

        return text

    def target_postprocessing(self, texts, special_tokens):
        if not isinstance(texts, list):
            texts = [texts]

        new_texts = []
        for text in texts:
            text = self.skip_special_tokens(text, special_tokens)

            for k, v in self.tokens_map.items():
                text = text.replace(k, v)

            new_texts.append(text)

        return new_texts

    def generation_function(self, texts):
        logger.info("Generation started..")
        _inputs = texts if isinstance(texts, list) else [texts]
        inputs = [self.prefix + inp for inp in _inputs]
        inputs = self.tokenizer(
            inputs,
            max_length=256,
            padding="max_length",
            truncation=True,
            return_tensors="jax",
        )

        input_ids = inputs.input_ids
        attention_mask = inputs.attention_mask
        logger.info("Generation started2..")
        output_ids = self.model.generate(
            input_ids=input_ids, attention_mask=attention_mask, **self.generation_kwargs
        )
        generated = output_ids.sequences
        logger.info("Generation postprocessing..")
        generated_recipe = self.target_postprocessing(
            self.tokenizer.batch_decode(generated, skip_special_tokens=False),
            self.special_tokens,
        )

        # TODO Save generated recipe to Database

        for text in generated_recipe:
            sections = text.split("\n")
            for section in sections:
                section = section.strip()
                if section.startswith("title:"):
                    section = section.replace("title:", "")
                    headline = "TITLE"
                elif section.startswith("ingredients:"):
                    section = section.replace("ingredients:", "")
                    headline = "INGREDIENTS"
                elif section.startswith("directions:"):
                    section = section.replace("directions:", "")
                    headline = "DIRECTIONS"

                if headline == "TITLE":
                    print(f"[{headline}]: {section.strip().capitalize()}")
                else:
                    section_info = [
                        f"  - {i+1}: {info.strip().capitalize()}"
                        for i, info in enumerate(section.split("--"))
                    ]
                    print(f"[{headline}]:")
                    print("\n".join(section_info))

            print("-" * 130)

        return generated_recipe
