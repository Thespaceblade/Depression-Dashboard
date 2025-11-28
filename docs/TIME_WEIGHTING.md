# Time-Weighted Depression Algorithm

## Overview

The depression calculator now uses **time-based weighting** to reflect that recent events have much more emotional impact than older ones. A loss that just happened is devastating, but the pain fades over time.

## How It Works

### Time Decay Function

Events are weighted using exponential decay:
- **Just happened (0 hours)**: 100% weight (full impact)
- **6 hours ago**: 78% weight
- **12 hours ago**: 61% weight
- **1 day ago**: 61% weight
- **2 days ago**: 37% weight
- **3 days ago**: 22% weight
- **4 days ago**: 14% weight
- **5+ days ago**: < 8% weight

### Special Cases

**Very Recent Events (within 6 hours):**
- Get a 20% boost to weight
- A DNF that just happened = maximum devastation
- A loss from yesterday still hurts, but less

**Recent Losing Streaks:**
- Consecutive losses within 1-2 days get 30% extra pain
- Recent losses in a streak compound the depression

## Examples

### Example 1: Max Verstappen DNF

**Scenario A: DNF just happened (0 hours ago)**
- Base DNF penalty: 12 points
- Time weight: 1.0 (100%)
- Recent boost: +20%
- **Total: 14.4 points** 💀

**Scenario B: DNF 2 days ago**
- Base DNF penalty: 12 points
- Time weight: 0.37 (37%)
- **Total: 4.4 points** 😔

**Scenario C: DNF 5 days ago**
- Base DNF penalty: 12 points
- Time weight: 0.08 (8%)
- **Total: 1.0 points** 😐

### Example 2: Cowboys Loss to Eagles (Rivalry)

**Scenario A: Just lost (0 days ago)**
- Base loss: 5 points
- Rivalry multiplier: 2.5x
- Time weight: 1.0
- **Total: 12.5 points** 😢

**Scenario B: Lost 2 days ago**
- Base loss: 5 points
- Rivalry multiplier: 2.5x
- Time weight: 0.37
- **Total: 4.6 points** 😐

**Scenario C: Lost 1 week ago**
- Base loss: 5 points
- Rivalry multiplier: 2.5x
- Time weight: 0.05
- **Total: 0.6 points** 😊

### Example 3: Recent Losing Streak

**Scenario: Lost 3 games in a row (0, 1, 2 days ago)**
- Game 1 (0 days): 3 points × 1.0 × 1.3 = 3.9 points
- Game 2 (1 day): 3 points × 0.61 × 1.3 = 2.4 points
- Game 3 (2 days): 3 points × 0.37 = 1.1 points
- **Total: 7.4 points** 😔

**Same streak but 1 week old:**
- Game 1 (7 days): 3 points × 0.03 = 0.1 points
- Game 2 (8 days): 3 points × 0.02 = 0.1 points
- Game 3 (9 days): 3 points × 0.01 = 0.0 points
- **Total: 0.2 points** 😊

## Impact on Depression Score

The time-weighting means:

1. **Recent events dominate** - A bad week can spike your depression
2. **Old events fade** - Past losses don't haunt you forever
3. **Fresh wounds hurt more** - A loss today is way worse than a loss last week
4. **Recovery is possible** - Good recent results can offset old bad ones

## Configuration

The decay rate can be adjusted in the code:
- `decay_rate=0.5` (default) - Moderate decay
- `decay_rate=0.3` - Slower decay (events stay relevant longer)
- `decay_rate=0.7` - Faster decay (events fade quickly)

## Real-World Example

**Monday**: Cowboys lose to Eagles (rivalry)
- Depression: +12.5 points (just happened)

**Tuesday**: Still thinking about it
- Depression: +4.6 points (1 day old, 37% weight)

**Wednesday**: Starting to move on
- Depression: +1.7 points (2 days old, 14% weight)

**Next Monday**: Old news
- Depression: +0.2 points (1 week old, 2% weight)

This reflects how real emotions work - fresh pain is intense, but time heals!

