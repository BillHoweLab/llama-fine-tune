# Llama-2 Fine-tuning

## With EC2

1. Upload the ready-to-train data to S3. We provide an example notebook for doing so with two datasets:
  * [Councils in Action Dataset](https://github.com/councildataproject/cdp-data)
  * [Huggingface English Quotes](https://huggingface.co/datasets/Abirate/english_quotes)

2. Use GitHub Actions to train a new model.

## Using Colab

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/billhowelab/llama-fine-tune/blob/main/notebooks/colab.ipynb)

Follow the steps laid out in the [./notebooks/colab.ipynb](./notebooks/colab.ipynb) notebook.