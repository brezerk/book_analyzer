# Input format

The market data log contains one message per line (terminated by a single line feed character, '\n' in C or
Java), and each message is a series of fields separated by spaces.

## Fields

| Timestamp   | Order action | Order ID | Side                   | Price | Size |
| ----------- | ------------ | -------- | -----------------------| ----- | ---- |
| int         | `A` - Add    | char     | `B` - Bid (buy order)  | int   | int  |
| int         | `A` - Add    | char     | `S` - Ask (sell order) | int   | int  |
| int         | `R` - Remove | char     |                        |       | int  |

## Examples

| Message                    | Decode                                          |
| -------------------------- | ----------------------------------------------- |
| `28800538 A b S 44.26 100` | Add order, id: `b`, Ask, 44.26$, for 100 shares |
| `28800562 A c B 44.10 100` | Add order, id: `c`, Bid, 44.10$, for 100 shares |
| `28800744 R b 100`         | Remove order, id: `b`, for 100 shares           |

