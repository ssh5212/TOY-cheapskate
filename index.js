let a = {}

let b = {a:1, b:2}
let c = {a:3, b:4}

a = b

a = c

document.write(a.b, a.c)