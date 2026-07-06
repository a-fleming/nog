# nog

`nog` is a small Advent of Code helper CLI for managing puzzle workflows from the terminal.

The goal is to reduce friction while solving Advent of Code challenges: fetch inputs, scaffold solution files, run local solutions, and eventually submit or validate answers without constantly switching back to the browser.

## Status

Early development. The project now has a `src/nog` package structure, an argparse-based CLI scaffold, local session record storage, and pytest coverage for session handling and CLI command behavior.

As of `v0.2.0`, `nog` includes the first usable authentication workflow:

- `nog auth login` opens a browser-assisted Advent of Code login flow.
- Users can log in with their preferred Advent of Code login provider.
- `nog` extracts the Advent of Code session cookie after login succeeds.
- The session is saved locally as a normalized session record for future commands.
- A development-only login path is available for local testing.

Puzzle fetching, input downloading, solution scaffolding, running, validation, and answer submission are not implemented yet.

## Current Command Shape

```sh
nog auth login
```

Development-only:

```sh
nog auth login --dev
```

The `--dev` option is intended for local development and testing. It is not part of the normal user workflow.

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

Puzzle inputs, cached puzzle text, session records, and other local Advent of Code data should stay local and should not be committed to public repositories.
