┌────────────────────────────────────┐
│            FRONTEND                │
│             Next.js                │
├────────────────────────────────────┤
│ • Prompt input                     │
│ • Interactive graph                │
│ • Equation display                 │
│ • AI explanation panel             │
│ • Parameter sliders(optional)      │
│ • Loading states                   │
└────────────────────────────────────┘
                 ↓ HTTP

┌────────────────────────────────────┐
│             BACKEND                │
│             FastAPI                │
├────────────────────────────────────┤
│ • Prompt endpoint                  │
│ • AI orchestration ✓               │
│ • Equation validation              │
│ • Numerical solving                │
│ • Graph data generation            │
│ • JSON response ✓                  │
└────────────────────────────────────┘
                 ↓

┌────────────────────────────────────┐
│              AI LAYER              │
├────────────────────────────────────┤
│ • Groq API ✓                       │
│ • Prompt parsing                   │
│ • Equation generation ✓            │
│ • Explanation generation           │
└────────────────────────────────────┘
                 ↓

┌────────────────────────────────────┐
│        EQUATION PROCESSING         │
├────────────────────────────────────┤
│ • SymPy parsing ★                  │
│ • Safe expression handling         │
│ • Equation validation              │
│ • Initial condition extraction     │
└────────────────────────────────────┘
                 ↓

┌────────────────────────────────────┐
│         NUMERICAL SOLVER           │
├────────────────────────────────────┤
│ • SciPy solve_ivp                  │
│ • NumPy                            │
│ • ODE integration                  │
│ • Time series generation           │
└────────────────────────────────────┘
                 ↓

┌────────────────────────────────────┐
│         VISUALIZATION DATA         │
├────────────────────────────────────┤
│ • x/y coordinate generation        │
│ • Animation frames                 │
│ • Plotly-compatible JSON           │
└────────────────────────────────────┘