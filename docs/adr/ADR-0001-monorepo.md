# ADR-0001: Monorepo

## Status
Accepted

## Context
OpenAutoHAB AI has tightly-coupled workflow requirements: discovery -> recommendations -> approval -> execution -> rollback.

## Decision
Use monorepo with clear service directories and shared docs.

## Consequences
Simpler cross-service changes and release management, at cost of larger repository.
