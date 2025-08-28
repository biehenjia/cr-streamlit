import streamlit as st
import pandas as pd
import benchmarking
from streamlit_ace import st_ace
import re

import app as pycr
def mtp(expr):
    expr = re.sub(r'\^', r'**', expr)
    expr = re.sub(r'(?<![\w.])(\d+)(?![\w.])', r'\1.0', expr)

    return expr

# Optional: global defaults that apply to every page unless overridden
st.set_page_config(page_title="CR Demo", page_icon="")

# ---- Session state bootstrap (safe to call every run)
st.session_state.setdefault("df", None)

# ---- Define pages as callables (or use file paths)
def home():
    st.title("chains of recurrences (`py_cr`)")
    st.markdown("the application of chains of recurrences (CR's) was used initially as an effective method to evaluate functions at regular intervals. ")
    st.markdown("view everything related to `py_cr` here:")
    st.page_link(gettingstarted_page, label="getting started `IN PROGRESS`", icon=":material/download:")
    st.page_link(gettingstarted_page, label="about chains `IN PROGRESS`", icon=":material/book_2:")
    st.page_link(staticexamples_page, label="examples", icon=":material/science:")
    st.page_link(benchmark_page, label="code generation", icon=":material/code_blocks:")

def gettingstarted():
    st.title("getting started")
    st.markdown("currently the package is under construction, but you can install beta wheels at `pip install py-chains-of-recurrences` for version `>=3.10`")
# ---- EXAMPLES START -----------
example_options = {"$\\text{trig}(n=1)$":{"expr":"2*sin(x)^2+2*cos(x)^2","params":"x,0,1,10"},
               "$\\text{trig}(n \geq 1)$":{"expr":"2*sin(x+y)^2+3*x+cos(y)","params":"x,0,1,10; y,0,1,10"},
               "$\\text{poly}(n = 1)$":{"expr":"x^5+x^4+x^3+x^2+x","params":"x,0,1,10"},
               "$\\text{poly}(n\geq 1)$":{"expr":"(x+y)*(x-y)","params":"x,0,1,10; y,0,1,10"},
               "$\\text{exp}(n= 1)$":{"expr":"1.01^x-exp(x)","params":"x,0,1,10"},
               "$\\text{exp}(n \geq 1)$":{"expr":"exp(x)-exp(y)","params":"x,0,1,10; y,0,1,10"}}

def applyexample():
    name = st.session_state.ex_name
    data = example_options.get(name)
    if not data:
        return
    st.session_state.update({
        "expr" : data.get("expr",""),
        "params" : data.get("params","")
    })

def staticexamples():
    
    st.title("examples")

    st.markdown("`eval_cr` accepts an expression and parameters in iterable format. Each parameter should be of the form $p=(x,x_0,h,i)$, where $x$ is the symbol, $x_0$ is the starting quantity, $h$ is the step, and $i$ is the iteration count. For the demo, use $;$ to delimit parameters. Please try to limit cycle variables to less than $10^7$")
    choice = st.pills("select a preset or input your own",example_options,key="ex_name",on_change=applyexample)
    SE_i1,SE_i2 = st.columns(2)
    SE_expr = SE_i1.text_input("Expression:",key="expr")
    SE_cycle = SE_i2.text_input("Cycle variable: ",key="params")
    
    if st.button("Evaluate Expression"):
        
        result, time_taken = pycr.evalcr(SE_expr, SE_cycle.split(";"))
        topy = mtp(SE_expr)
        r2, t2 = benchmarking.bench_blocks_py(topy, SE_cycle)
        r3, t3 = benchmarking.bench_blocks_subs(topy,SE_cycle)
        df = pd.DataFrame({"method":["pycr (sequential)", "compiled + vectorized (SIMD)", "naive"],
                        "time (ms)":[time_taken, t2, t3], 
                        "1st value":[result[0],r2[0],r3[0]],
                        "2nd value":[None,None,None],
                        "last value":[result[-1],r2[-1],r3[-1]]
                        })
        if len(result) > 1:
            df["2nd value"] = [result[1], r2[1], r3[1]]
        st.dataframe(df)
    
        #st.error("Error occurred during benchmarking!")
    # WRITE TO SUBPROCESS WITH MAX TIMER 
    st.divider()
    st.page_link(home_page, label="home", icon=":material/home:")

# ---- EXAMPLES END -----------




# ----- BENCHMARK SANDBOX START --------

def benchmark(): 
    st.title("code generation")
    st.markdown("enter expression and parameters below. For more information on formatting, view examples.")
    choice = st.pills("select a preset or input your own",example_options,key="ex_name",on_change=applyexample)
    SE_i1,SE_i2 = st.columns(2)
    SE_expr = SE_i1.text_input("Expression:",key="expr")
    SE_cycle = SE_i2.text_input("Cycle variable: ",key="params")
    if st.button("Generate Code"):
        try:

            code, time_taken = pycr.crgen(SE_expr, SE_cycle.split(";"))
            st.code(code)
        except:
            st.error("Error occurred during generation!")
    
    # content = st_ace(theme="twilight", auto_update=True)
    # if st.button("Run Code"):
    #     # response = init(f"{content}\nprint(A1[0])")
    #     response = init("print('hello World!')")
    #     st.write(f"list value: {response['stdout']}")
    # st.divider()
    st.page_link(home_page, label="home", icon=":material/home:")
# ----- BENCHMARK SANDBOX END --------


# ----- GETTING STARTED WHEELS --------


# ---- Wrap pages with metadata
home_page = st.Page(home, title="Home", icon=":material/home:")
gettingstarted_page = st.Page(gettingstarted, title = "Getting Started", icon = ":material/settings:")
staticexamples_page = st.Page(staticexamples, title = "Static Examples", icon = ":material/science:")
benchmark_page = st.Page(benchmark, title = "Benchmarks", icon = ":material/code_blocks:")



# MAYBE USE ST.METRIC??? 

# ---- Build the nav (top or sidebar). Sections are optional.
pages = {
    "Other Pages":   [home_page,   gettingstarted_page,staticexamples_page, benchmark_page],
}
pg = st.navigation(pages, position="top")  # or "sidebar"
pg.run()
