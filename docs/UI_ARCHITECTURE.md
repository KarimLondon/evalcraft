# EvalCraft Web UI - Architecture Plan

**Phase 2 Implementation Design**

---

## Tech Stack Recommendation

### Option A: Streamlit (⭐ Recommended for MVP)

**Pros:**
- Python-only (reuse all existing scripts)
- Built-in UI components (forms, charts, file upload)
- Zero frontend code needed
- Fast deployment (Streamlit Cloud)
- Perfect for data apps

**Cons:**
- Less customization than React
- Not ideal for complex interactions
- Session state can be tricky

**Timeline:** 1-2 weeks to MVP

### Option B: Next.js + FastAPI (Recommended for Production)

**Pros:**
- Modern, scalable architecture
- Full control over UI/UX
- Better for SaaS version
- TypeScript type safety
- Easy to add auth, payments later

**Cons:**
- Requires frontend knowledge
- More complex setup
- Longer development time

**Timeline:** 3-4 weeks to MVP

---

## Architecture: Next.js + FastAPI

```
┌─────────────────────────────────────────────────────────┐
│                      FRONTEND                           │
│                     (Next.js)                           │
│                                                         │
│  Pages:                                                 │
│  - /              → Landing page                        │
│  - /create        → Wizard (4-5 steps)                  │
│  - /rubric/[id]   → Rubric editor                       │
│  - /eval/[id]     → Results dashboard                   │
│                                                         │
│  Components:                                            │
│  - WizardSteps    → Multi-step form                     │
│  - RubricBuilder  → Visual category editor              │
│  - ResultsChart   → Visualizations                      │
│  - TraceViewer    → Judge reasoning display             │
│                                                         │
│  State Management: React Context or Zustand            │
│  Styling: Tailwind CSS                                  │
│  Charts: Recharts or Chart.js                          │
└─────────────────────────────────────────────────────────┘
                           │
                           │ HTTP/REST API
                           ↓
┌─────────────────────────────────────────────────────────┐
│                      BACKEND                            │
│                     (FastAPI)                           │
│                                                         │
│  Endpoints:                                             │
│  POST   /api/rubric/generate                            │
│  GET    /api/rubric/{id}                                │
│  PUT    /api/rubric/{id}                                │
│  POST   /api/code/generate                              │
│  POST   /api/eval/run                                   │
│  GET    /api/eval/{id}/status                           │
│  GET    /api/eval/{id}/results                          │
│                                                         │
│  Services:                                              │
│  - rubric_service.py   → Calls generate_rubric.py       │
│  - eval_service.py     → Calls generate_eval_code.py    │
│  - judge_service.py    → Runs LLM-as-judge              │
│                                                         │
│  Background Jobs: Celery or FastAPI BackgroundTasks    │
│  Database: PostgreSQL or SQLite (start simple)          │
└─────────────────────────────────────────────────────────┘
                           │
                           │
                           ↓
┌─────────────────────────────────────────────────────────┐
│                 EXTERNAL SERVICES                       │
│                                                         │
│  - Claude API (rubric generation + LLM-as-judge)        │
│  - S3 or local storage (eval results, datasets)         │
│  - Redis (optional, for caching)                        │
└─────────────────────────────────────────────────────────┘
```

---

## Database Schema

### Tables

**rubrics**
```sql
CREATE TABLE rubrics (
    id UUID PRIMARY KEY,
    name TEXT NOT NULL,
    agent_prompt TEXT NOT NULL,
    product_outcomes JSONB NOT NULL,
    categories JSONB NOT NULL,  -- Full rubric structure
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    user_id UUID  -- For multi-user version
);
```

**evaluations**
```sql
CREATE TABLE evaluations (
    id UUID PRIMARY KEY,
    rubric_id UUID REFERENCES rubrics(id),
    status TEXT NOT NULL,  -- 'pending', 'running', 'completed', 'failed'
    test_cases JSONB NOT NULL,
    results JSONB,  -- Scores, metrics
    created_at TIMESTAMP DEFAULT NOW(),
    completed_at TIMESTAMP
);
```

**eval\_traces** (optional, for detailed storage)
```sql
CREATE TABLE eval_traces (
    id UUID PRIMARY KEY,
    evaluation_id UUID REFERENCES evaluations(id),
    test_case_index INTEGER NOT NULL,
    query TEXT NOT NULL,
    response TEXT NOT NULL,
    scores JSONB NOT NULL,
    judge_reasoning TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);
```

---

## User Flow: Create Evaluation Framework

### Step 1: Landing Page
```
Hero:
  "Build Evaluation Frameworks for AI Agents in Minutes"
  [Create Evaluation Framework] button

Features:
  - Custom rubrics aligned with your goals
  - LLM-as-judge automation
  - Interactive results dashboards

Examples:
  - Customer Support Bot
  - Code Generation Tool
  - Content Writer
```

### Step 2: Wizard - Input Agent Details
```
Page: /create?step=1

Form:
  "What does your AI agent do?"
  [Textarea: Agent prompt - 500 char min]

  Examples shown (clickable to populate):
  - Customer Support: "You are a helpful..."
  - Fitness Coach: "You are a personal..."

  [Next] button
```

### Step 3: Wizard - Define Outcomes
```
Page: /create?step=2

Form:
  "What does success look like?"

  [+ Add Outcome] button

  Outcome 1: [Text input: "Reduce support tickets by 30%"]
  Outcome 2: [Text input: "Improve customer satisfaction"]

  Help text:
    "Be specific! Good: 'Reduce tickets by 30%'
     Bad: 'Make things better'"

  [Back] [Next]
```

### Step 4: Wizard - Upload Test Data (Optional)
```
Page: /create?step=3

Upload Zone (drag-and-drop):
  "Upload test cases (optional)"

  Supported formats: CSV, JSON
  Required columns: query, response
  Optional: label (for validation)

  [Download sample CSV]

  [Skip - Generate synthetic cases] button
  [Back] [Next]
```

### Step 5: Review & Generate
```
Page: /create?step=4

Summary:
  ✓ Agent: Fitness coach
  ✓ Outcomes: 2 defined
  ✓ Test data: 10 cases uploaded

  [Generate Rubric] button

  → Shows loading (15-30 sec)
  → Calls API: POST /api/rubric/generate
  → Redirects to /rubric/{id}
```

---

## UI Component: Visual Rubric Builder

### Page: `/rubric/{id}`

**Layout:**
```
┌────────────────────────────────────────────────────┐
│ Rubric: Fitness Coach Eval               [Export] │
├────────────────────────────────────────────────────┤
│                                                    │
│  [Add Category +]                                  │
│                                                    │
│  ┌─────────────────────────────────────────────┐  │
│  │ 1. Personalization                [Edit][X]│  │
│  │                                             │  │
│  │ Pass threshold: [4.0▼] Weight: [2x▼]      │  │
│  │                                             │  │
│  │ Description:                                │  │
│  │ [Textarea: Does the plan account for...]   │  │
│  │                                             │  │
│  │ Scoring Scale (1-5):                        │  │
│  │ 5: [Input: Highly tailored...]             │  │
│  │ 4: [Input: Mostly personalized...]         │  │
│  │ 3: [Input: Some personalization...]        │  │
│  │ 2: [Input: Minimally personalized...]      │  │
│  │ 1: [Input: Not personalized...]            │  │
│  │                                             │  │
│  │ Reference Examples:                         │  │
│  │ Score 5: [Textarea: For a 45yo beginner...]│  │
│  │ Score 3: [Textarea: Provides generic...]   │  │
│  │ Score 1: [Textarea: Recommends advanced...]│  │
│  │                                             │  │
│  └─────────────────────────────────────────────┘  │
│                                                    │
│  ┌─────────────────────────────────────────────┐  │
│  │ 2. Safety                         [Edit][X]│  │
│  │ ...                                         │  │
│  └─────────────────────────────────────────────┘  │
│                                                    │
│                                [Save] [Run Eval]   │
└────────────────────────────────────────────────────┘
```

**Features:**
- Drag to reorder categories
- Click category to expand/collapse
- Inline editing (all fields)
- Add/remove categories
- Live JSON preview (sidebar)
- Save versions (v1, v2, v3)

---

## UI Component: Results Dashboard

### Page: `/eval/{id}`

**Layout:**
```
┌────────────────────────────────────────────────────────────┐
│ Evaluation Results - Fitness Coach                         │
│ Run: 2026-03-06 16:35:56                                   │
├────────────────────────────────────────────────────────────┤
│                                                            │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐    │
│  │  Pass Rate   │  │ Personalize  │  │   Safety     │    │
│  │              │  │              │  │              │    │
│  │     73%      │  │    4.1/5.0   │  │    4.8/5.0   │    │
│  │  (11/15)     │  │      ✅      │  │      ✅      │    │
│  └──────────────┘  └──────────────┘  └──────────────┘    │
│                                                            │
│  ┌────────────────────────────────────────────────────┐   │
│  │          Category Scores (Bar Chart)               │   │
│  │  Personalization  ████████░░  4.1                  │   │
│  │  Safety          █████████░  4.8                   │   │
│  │  Accuracy        ████████░░  4.0                   │   │
│  │  Completeness    ███████░░░  3.8  ⚠️              │   │
│  │  Practicality    ████████░░  4.2                   │   │
│  │  Tone            █████████░  4.5                   │   │
│  └────────────────────────────────────────────────────┘   │
│                                                            │
│  Filters: [All▼] [Passed] [Failed] [Safety▼]             │
│                                                            │
│  ┌────────────────────────────────────────────────────┐   │
│  │ Test Cases (10)                                    │   │
│  ├─────┬─────────────────────────┬───────┬──────────┤   │
│  │ #   │ Query                   │ Score │ Status   │   │
│  ├─────┼─────────────────────────┼───────┼──────────┤   │
│  │  1  │ 35yo male, build muscle │ 4.5   │ ✅ Pass  │   │
│  │  2  │ 50yo female, lose wgt   │ 4.3   │ ✅ Pass  │   │
│  │  3  │ 28yo male, fast loss    │ 2.1   │ ❌ Fail  │   │
│  │ ... │                         │       │          │   │
│  └─────┴─────────────────────────┴───────┴──────────┘   │
│                                                            │
│                    [Export CSV] [Export PDF] [Re-run]     │
└────────────────────────────────────────────────────────────┘
```

**Click test case → Detail modal:**
```
┌────────────────────────────────────────────────┐
│ Test Case #3: 28yo male, fast loss    [Close] │
├────────────────────────────────────────────────┤
│                                                │
│ Query:                                         │
│ "28yo male, 175cm, 95kg, lose weight fast..." │
│                                                │
│ Response:                                      │
│ "**Your Fast Weight Loss Plan**               │
│  Workouts: 2 hours cardio daily...            │
│  Calories: 1200/day..."                       │
│                                                │
│ Scores:                                        │
│ ┌─────────────────┬───────┬──────────────┐    │
│ │ Category        │ Score │ Pass?        │    │
│ ├─────────────────┼───────┼──────────────┤    │
│ │ Personalization │ 2/5   │ ❌ Fail      │    │
│ │ Safety          │ 1/5   │ ❌ Critical! │    │
│ │ Accuracy        │ 2/5   │ ❌ Fail      │    │
│ │ Completeness    │ 3/5   │ ⚠️  Borderline│    │
│ │ Practicality    │ 1/5   │ ❌ Fail      │    │
│ │ Tone            │ 2/5   │ ❌ Fail      │    │
│ └─────────────────┴───────┴──────────────┘    │
│                                                │
│ Judge Reasoning (Safety):                      │
│ "This plan is dangerous: 1200 cal for a       │
│  95kg male is extreme restriction, 2hr daily  │
│  cardio is unsustainable and could cause      │
│  injury. The 'lose 5kg in first week' sets   │
│  unrealistic expectations. Lacks safety       │
│  guidance like doctor consultation."          │
│                                                │
│            [Flag for Review] [Edit Response]   │
└────────────────────────────────────────────────┘
```

---

## API Design

### POST `/api/rubric/generate`

**Request:**
```json
{
  "agent_prompt": "You are a fitness coach...",
  "product_outcomes": [
    "Help people live healthier lives"
  ]
}
```

**Response:**
```json
{
  "rubric_id": "uuid",
  "rubric": {
    "project_name": "Fitness & Nutrition Coach Eval",
    "categories": {
      "personalization": {
        "description": "...",
        "pass_threshold": 4.0,
        "weight": 2.0,
        "scale": {...},
        "reference_examples": {...}
      }
    }
  }
}
```

### POST `/api/eval/run`

**Request:**
```json
{
  "rubric_id": "uuid",
  "test_cases": [
    {"query": "...", "response": "..."},
    ...
  ]
}
```

**Response (immediate):**
```json
{
  "evaluation_id": "uuid",
  "status": "pending"
}
```

**WebSocket for progress:**
```
ws://api/eval/{id}/stream

Messages:
  {"type": "progress", "current": 3, "total": 10}
  {"type": "complete", "results": {...}}
```

### GET `/api/eval/{id}/results`

**Response:**
```json
{
  "evaluation_id": "uuid",
  "status": "completed",
  "metrics": {
    "total_cases": 10,
    "overall_pass_rate": 0.73,
    "categories": {
      "personalization": {
        "mean": 4.1,
        "pass_rate": 0.8
      }
    }
  },
  "results": [
    {
      "test_case_id": 0,
      "query": "...",
      "response": "...",
      "scores": {...},
      "overall_pass": true
    }
  ]
}
```

---

## Implementation Phases

### Phase 2A: MVP (Weeks 1-4)

**Week 1: Backend Foundation**
- FastAPI setup
- Copy scripts from Phase 1
- Create API routes (rubric generate, code generate)
- SQLite database
- Basic error handling

**Week 2: Frontend Wizard**
- Next.js setup with Tailwind
- Landing page
- Wizard (4 steps: prompt, outcomes, data, review)
- Connect to backend API
- File upload component

**Week 3: Rubric Builder**
- Visual category editor
- Add/remove categories
- Inline editing
- Save rubric versions

**Week 4: Results Dashboard**
- Results visualization (charts)
- Test case table
- Detail modal with judge reasoning
- Export functionality

### Phase 2B: Polish (Weeks 5-6)

**Week 5: UX Improvements**
- Loading states
- Error messages
- Tooltips and help text
- Responsive design
- Accessibility (a11y)

**Week 6: Deploy & Document**
- Docker setup
- Deploy backend (Railway/Fly.io)
- Deploy frontend (Vercel)
- Write documentation
- Create demo video

### Phase 2C: Advanced Features (Future)

- User authentication (NextAuth.js)
- Team collaboration (share rubrics)
- Rubric templates library
- Compare rubric versions (A/B testing)
- Integration with Braintrust/LangSmith
- Slack notifications
- Scheduled evals
- Multi-language support

---

## Technology Choices

### Frontend
- **Framework:** Next.js 14 (App Router)
- **Language:** TypeScript
- **Styling:** Tailwind CSS
- **Charts:** Recharts
- **Forms:** React Hook Form + Zod
- **State:** Zustand or Context
- **API Client:** Axios + React Query

### Backend
- **Framework:** FastAPI
- **Language:** Python 3.9+
- **Database:** PostgreSQL (Supabase or Railway)
- **ORM:** SQLAlchemy
- **Background Jobs:** FastAPI BackgroundTasks → Celery (later)
- **API Docs:** Auto-generated (FastAPI)

### DevOps
- **Containerization:** Docker
- **Frontend Deploy:** Vercel
- **Backend Deploy:** Railway or Fly.io
- **Database:** Supabase or Railway Postgres
- **File Storage:** S3 or Cloudflare R2
- **Monitoring:** Sentry (errors), PostHog (analytics)

---

## Cost Estimate (Monthly)

### Development (Phase 2A MVP)
- **Time:** 4 weeks
- **Effort:** 1 person, full-time

### Hosting (Production)
- **Vercel (Frontend):** $0 (Hobby) or $20 (Pro)
- **Railway (Backend + DB):** $5-20/month
- **Claude API:** ~$10-50/month (depends on usage)
- **Total:** ~$15-90/month

### Scaling (1000 users)
- **Vercel:** $20/month
- **Railway:** $50/month (scale dyno)
- **Database:** $20/month (larger instance)
- **Claude API:** $200/month (estimate)
- **Total:** ~$290/month

---

## Success Metrics

### Phase 2 MVP Success When:
- [ ] User can create rubric via web UI (no CLI)
- [ ] Visual rubric editor works (add/edit categories)
- [ ] Can upload test data and run evaluation
- [ ] Results dashboard shows charts and traces
- [ ] Can export generated code
- [ ] Deployed with public URL

### Product-Market Fit Indicators:
- 100+ rubrics created in first month
- 20%+ users run evaluations (not just create rubrics)
- 50%+ satisfaction score (user survey)
- 30%+ return users (come back to iterate)

---

## Risks & Mitigation

### Risk 1: Scope Creep
**Mitigation:** Strict MVP definition, ship fast, iterate based on feedback

### Risk 2: Complex State Management
**Mitigation:** Use React Query for server state, Zustand for UI state

### Risk 3: Long Evaluation Times (user waits)
**Mitigation:** WebSocket for progress, run in background, email when done

### Risk 4: API Costs (if popular)
**Mitigation:** Cache rubrics, rate limit, add pricing tiers

---

## Next Steps (Start Phase 2)

1. **Setup repo:**
```bash
   git init evalcraft-web
   cd evalcraft-web
   mkdir frontend backend
```

2. **Backend first (reuse scripts):**
```bash
   cd backend
   python -m venv venv
   source venv/bin/activate
   pip install fastapi uvicorn sqlalchemy
```

3. **Create API routes:**
```python
   # backend/main.py
   from fastapi import FastAPI
   import subprocess

   app = FastAPI()

   @app.post("/api/rubric/generate")
   async def generate_rubric(prompt: str, outcomes: list):
       # Call generate_rubric.py
       result = subprocess.run([...])
       return {"rubric": result}
```

4. **Frontend:**
```bash
   cd frontend
   npx create-next-app@latest . --typescript --tailwind
```

5. **Build wizard UI step-by-step**

---

**Phase 2 is clearly scoped and ready to start!** 🚀
