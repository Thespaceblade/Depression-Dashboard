# Opponent Context Algorithm

The depression calculator now considers **who you lost to** when calculating depression. Not all losses are created equal!

## How It Works

### Opponent Quality Multipliers

**For Non-Rival Losses:**
- **Losing to a great team (65%+ win rate)**: 0.6x multiplier
  - "They're really good, expected loss"
  - Example: Losing to Chiefs (11-1) = less painful
  
- **Losing to a good team (55-65% win rate)**: 0.8x multiplier
  - "They're solid, understandable loss"
  
- **Losing to an average team (45-55% win rate)**: 1.0x multiplier
  - Standard loss penalty
  
- **Losing to a below-average team (35-45% win rate)**: 1.2x multiplier
  - "We should have won that"
  
- **Losing to a bad team (<35% win rate)**: 1.5x multiplier
  - "We lost to THEM?!" (embarrassing!)

### Rivalry Losses

Rivalry losses always hurt more, but opponent quality still matters:

- **Losing to a bad rival (<35% win rate)**: 2.2x multiplier 💀
  - "We lost to THEM?! And they're our RIVAL?!"
  - Most painful scenario
  
- **Losing to a below-average rival (35-45%)**: 2.0x multiplier
  - Very disappointing
  
- **Losing to an average/good rival (45-65%)**: 1.8x multiplier
  - Standard rivalry pain
  
- **Losing to a great rival (65%+)**: 1.5x multiplier
  - Still hurts (it's a rival!), but they're good so it's understandable

### Win Context

**Beating a rival**: 1.5x bonus (feels extra good!)
**Beating a good team (60%+ win rate)**: 1.3x bonus (quality win!)

## Examples

### Example 1: Cowboys Losses

**Scenario A: Lose to Eagles (rival, great team 10-2 = 83%)**
- Base loss: 3.0 points
- Rival multiplier: 1.5x (great rival)
- **Total: 3.5 points** 😔

**Scenario B: Lose to Commanders (rival, bad team 3-10 = 23%)**
- Base loss: 3.0 points
- Rival multiplier: 2.2x (bad rival = embarrassing!)
- **Total: 4.5 points** 😢

**Scenario C: Lose to Chiefs (non-rival, great team 11-1 = 92%)**
- Base loss: 3.0 points
- Quality multiplier: 0.6x (they're really good)
- **Total: 2.1 points** 😐

**Difference**: Losing to bad rival (4.5) vs great non-rival (2.1) = **2.4x more painful!**

### Example 2: Warriors Losses

**Scenario A: Lose to Lakers (rival, good team 15-10 = 60%)**
- Base loss: 3.0 points
- Rival multiplier: 1.8x
- **Total: 4.1 points**

**Scenario B: Lose to Pistons (non-rival, bad team 5-20 = 20%)**
- Base loss: 3.0 points
- Quality multiplier: 1.5x (embarrassing!)
- **Total: 3.8 points**

Even though Pistons are worse, losing to Lakers (rival) hurts more!

## Configuration

To use opponent context, add to your `teams_config.json`:

```json
{
  "name": "Dallas Cowboys",
  "recent_streak": ["L", "W", "L"],
  "recent_opponents": ["Philadelphia Eagles", "New York Giants", "Washington Commanders"],
  "recent_opponent_records": [
    {"wins": 10, "losses": 2},
    {"wins": 6, "losses": 6},
    {"wins": 3, "losses": 10}
  ]
}
```

The arrays must match in length and order:
- `recent_streak[0]` = result vs `recent_opponents[0]` (with record `recent_opponent_records[0]`)

## Impact

This makes the algorithm much more realistic:
- ✅ Losing to good teams = less depression (expected)
- ✅ Losing to bad teams = more depression (embarrassing)
- ✅ Rivalry losses always hurt, but quality matters
- ✅ Beating rivals/good teams feels extra good

The calculator now understands that context matters!

