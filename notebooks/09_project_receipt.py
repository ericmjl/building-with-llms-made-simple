# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "litellm==1.73.6",
#     "llamabot[all]==0.12.11",
#     "marimo",
#     "pydantic==2.11.7",
#     "pyprojroot==0.3.0",
# ]
# ///

import marimo

__generated_with = "0.14.10"
app = marimo.App(width="medium")


@app.cell
def _():
    import llamabot as lmb
    from pydantic import BaseModel, Field
    from typing import List
    from pyprojroot import here
    import marimo as mo

    return BaseModel, Field, List, here, lmb, mo


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    # Generating structured outputs from images

    This one requires a vision language model.
    Of the VLMs that I've tried, GPT-4o works.
    Ollama models fail for a weird technical error.
    """
    )
    return


@app.cell
def _(BaseModel, Field, List, here, lmb):
    class Item(BaseModel):
        name: str = Field(description="Name of the item on the receipt.")
        quantity: int = Field(description="Number of items purchased", default=1)
        amount: float = Field(description="Total amount for this item.")

    class Receipt(BaseModel):
        items: List[Item]
        total_amount: float = Field(description="Total amount paid.")

    receipt_bot = lmb.StructuredBot(
        system_prompt="You are a skilled OCR bot for receipts.",
        pydantic_model=Receipt,
    )

    receipt = receipt_bot(lmb.user(here() / "notebooks" / "assets" / "receipt.webp"))
    return (receipt,)


@app.cell
def _(receipt):
    receipt.items
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
