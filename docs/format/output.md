# Output format

BookAnalyzer's output consists of one message per line, in the following format.

## Fields

| Timestamp   | Order action           | Size     |
| ----------- | ---------------------- | -------- |
| int         | `B` - Bid (buy order)  | int      |
| int         | `S` - Ask (sell order) | int      |

## Examples

| Message              | Decode                                                   |
| -------------------- | -------------------------------------------------------- |
| `28800758 S 8832.56` | The total expense for selling X shares would be 8832.56$ |
| `28800796 S NA`      | The total expense for selling X shares not avalible now  |
| `28800974 B 8865.00` | The total expense for buying X shares would be 8865.00$  |
| `28800974 B NA`      | The total expense for buying X shares not avalible now   |

