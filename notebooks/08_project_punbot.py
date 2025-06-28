import marimo

__generated_with = "0.14.5"
app = marimo.App(width="full")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    # Paul Ivanov Clone a.k.a. PIBot

    Paul Ivanov, a long-time attendee of the SciPy conference and one of the longest-running hosts of the Lightning Talks, is also well known to be a pun master.
    Unfortunately for us, Paul has stepped down from the role of lightning talk host.
    Let's reclaim some of Paul's magic by create a PIBot (Paul Ivanov Bot)
    that generates puns in response to the transcript of a lightning talk.

    I have left this project extremely open-ended, and as such I consider it to be one of the more advanced ones to pursue.
    But if you make it work, I'd encourage you to demo it at the Lightning Talks!
    """
    )
    return


@app.cell
def _():
    # Your code here!
    return


if __name__ == "__main__":
    app.run()
