# nog

`nog` is a small Advent of Code helper CLI for managing puzzle workflows from the terminal.

The goal is to reduce friction while solving Advent of Code challenges: fetch inputs, scaffold solution files, run local solutions, and eventually submit or validate answers without constantly switching back to the browser.

## Status

Early development. This project is experimental and will evolve as the workflow becomes clearer.

## Planned Direction

`nog` is intended to help with:

- Advent of Code authentication from the CLI
- fetching and caching puzzle inputs
- generating starter files from language templates
- running local solutions
- submitting answers
- tracking local progress by language
- avoiding duplicate or unnecessary submissions

## Example Usage

```sh
nog auth login
nog new 2024 1
nog submit 2024 1
```

The default workflow should stay simple, with options added over time for manual overrides such as language, puzzle part, or answer value.

## Notes

Puzzle inputs and cached puzzle text should stay local and should not be committed to public repositories.
