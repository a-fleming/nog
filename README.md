# nog

`nog` is a small Advent of Code helper CLI for managing puzzle workflows from the terminal.

The goal is to reduce friction while solving Advent of Code challenges: fetch inputs, scaffold solution files, run local solutions, and eventually submit or validate answers without constantly switching back to the browser.

## Status

Early development. The project now has a `src/nog` package structure and an initial argparse CLI scaffold, while Advent of Code session handling is still being prototyped. The current Playwright-based auth helper is development-only, and the public command workflow is still under construction.

## Planned Direction

`nog` is intended to help with:

- Advent of Code authentication from the CLI
- fetching and caching puzzle inputs
- generating starter files from language templates
- running local solutions
- submitting answers
- tracking local progress by language
- avoiding duplicate or unnecessary submissions

## Planned Command Shape

```sh
nog auth login
nog new 2024 1
nog submit 2024 1
```

The default workflow should stay simple, with options added over time for manual overrides such as language, puzzle part, or answer value.

## Notes

Puzzle inputs and cached puzzle text should stay local and should not be committed to public repositories.
