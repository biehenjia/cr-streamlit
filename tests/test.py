import py

expr = "a^2 + b^2"
params = ["a,1.0,2.0,3", "b,4.0,5.0,6"]
result, time_taken = py.evalcr(expr, params)
print(f"Result: {result}, Time taken: {time_taken} ms")