Add [num] Dis to [target] {sub check && ! tag ind:state}
Add [num] Adv to [target] {sub check && ! tag ind:state}
Sub [num] from [target] {sub check && ! tag specif:state}
Add [num] to [target] {sub check && ! tag specif:state}
Set {tag letter:state} to [dice/target/num] for (number) calls
Roll [dice]
Add token [token] to [target]
Hack [target program]
Token (number) statements