# EvalCraft Phase 2: Resumption Guide

**Created:** 2026-03-06
**Phase 1 Status:** ✅ Complete (Claude Skill MVP)
**Next Phase:** Web UI Implementation

---

## What Was Built (Phase 1)

### Complete Claude Code Skill
Location: `~/.claude/skills/evalcraft/`

**12 files created:**
- `SKILL.md` - Main orchestrator (conversation flow)
- `README.md` - Documentation
- `scripts/generate_rubric.py` - AI-powered rubric generation
- `scripts/generate_eval_code.py` - Code generator
- `templates/rubric_template.md` - Rubric structure
- `templates/eval_code_template.py` - Python eval framework (34KB)
- `references/eval_best_practices.md` - Synthesized knowledge
- `references/rubric_building_guide.md` - Step-by-step guide
- `references/llm_judge_patterns.md` - Implementation patterns
- `examples/sample_rubric.md` - Customer support example
- `examples/sample_eval_code.py` - Working example
- `examples/sample_dataset.csv` - Dataset format

### Test Validation
Location: `~/Documents/eval_projects/fitness_coach_eval/`

**Tested with fitness coach agent:**
- Generated custom 6-category rubric
- Created evaluation code (34KB standalone Python)
- Built 10-case test dataset
- Validated error handling

### Design Documentation
Location: `~/.claude/plans/compiled-twirling-grove.md`

**Complete implementation plan including:**
- Architecture overview
- Conversation flow (6 phases)
- Implementation components
- Design trade-offs
- Success criteria
- Phase 2 roadmap

---

## Phase 2: Web UI Roadmap

### Proposed Stack

**Option A: Streamlit (Fastest)**
- Python-based (reuse existing scripts)
- Built-in UI components
- Easy deployment (Streamlit Cloud)
- Timeline: 1-2 weeks

**Option B: Next.js + FastAPI (Production-ready)**
- React frontend (modern, scalable)
- Python backend (reuse scripts)
- Better for SaaS version
- Timeline: 3-4 weeks

### Key Features to Implement

1. **Home Page**
  - Explain what EvalCraft does
  - "Create Evaluation Framework" button
  - Example use cases

2. **Wizard Flow** (mirrors skill)
  - Step 1: Agent prompt input (textarea)
  - Step 2: Product outcomes input (bullet list)
  - Step 3: Upload labeled data (optional, drag-and-drop CSV)
  - Step 4: Review generated rubric (editable)
  - Step 5: Generate & download code OR run evaluation

3. **Rubric Builder** (visual)
  - Add/remove categories
  - Edit descriptions, scales, thresholds
  - Add reference examples
  - Live preview

4. **Evaluation Runner**
  - Upload test dataset
  - Run evaluation (progress bar)
  - View results dashboard
  - Download artifacts

5. **Results Dashboard**
  - Overall pass rate (gauge chart)
  - Per-category scores (bar chart)
  - Test cases table (sortable, filterable)
  - Click to view traces
  - Export results

### File Structure (Proposed)

```
evalcraft-web/
├── frontend/                    # Next.js or Streamlit
│   ├── pages/
│   │   ├── index.tsx           # Home
│   │   ├── create.tsx          # Wizard
│   │   ├── results/[id].tsx    # Results dashboard
│   ├── components/
│   │   ├── RubricBuilder.tsx   # Visual rubric editor
│   │   ├── WizardSteps.tsx     # Step-by-step form
│   │   ├── ResultsChart.tsx    # Visualizations
│   ├── lib/
│   │   ├── api.ts              # API client
├── backend/                     # FastAPI
│   ├── main.py                 # API routes
│   ├── services/
│   │   ├── rubric_service.py   # Reuse generate_rubric.py
│   │   ├── eval_service.py     # Reuse generate_eval_code.py
│   ├── models/
│   │   ├── rubric.py           # Data models
├── shared/                      # Reuse from skill
│   ├── generate_rubric.py      # Copy from skill
│   ├── generate_eval_code.py   # Copy from skill
│   ├── eval_code_template.py   # Copy from skill
├── docker-compose.yml
├── README.md
└── .env.example
```

### Integration Points

**Reuse from Phase 1:**
- `generate_rubric.py` - Call as-is from backend
- `generate_eval_code.py` - Call as-is from backend
- `eval_code_template.py` - Template for code generation
- `eval_best_practices.md` - Display in UI as tooltips/help
- All reference materials - Use for UI guidance text

**New for Phase 2:**
- Visual rubric editor component
- Real-time eval execution (WebSocket for progress)
- User authentication (if multi-user)
- Database (store rubrics, results)
- Deployment config (Docker, k8s)

---

## Phase 2 Implementation Steps

### Week 1: Setup & Core API
1. Create new repo: `evalcraft-web`
2. Set up FastAPI backend
3. Copy scripts from skill → `backend/services/`
4. Create API routes:
  - `POST /api/rubric/generate` (calls generate_rubric.py)
  - `POST /api/code/generate` (calls generate_eval_code.py)
  - `POST /api/eval/run` (executes evaluation)
  - `GET /api/eval/{id}/results` (returns results)

### Week 2: Frontend Wizard
1. Create Next.js/Streamlit app
2. Build wizard UI (4-5 steps)
3. Connect to backend API
4. File upload for test data
5. Download generated artifacts

### Week 3: Visual Rubric Builder
1. Drag-and-drop category reordering
2. Inline editing (descriptions, thresholds)
3. Add/remove categories
4. Reference example editor
5. Live JSON preview

### Week 4: Results Dashboard
1. Results visualization (charts)
2. Test case drill-down
3. Judge reasoning display
4. Export functionality
5. Compare rubric versions

### Week 5: Polish & Deploy
1. Error handling
2. Loading states
3. Responsive design
4. Documentation
5. Deploy (Vercel + Railway or Docker)

---

## Known Issues to Fix

### From Phase 1 Testing:

1. **Template syntax error** (FIXED manually, needs template update)
  - Line 603: `metrics: Dict[str, Any]],` → `metrics: Dict[str, Any],`
  - Fix in: `templates/eval_code_template.py`

2. **Empty results handling**
  - If all evals fail (API error), `min()` crashes on empty sequence
  - Fix in: `evaluate.py` line 841 (add check for empty categories)

3. **Progress indicators**
  - Currently just prints dots
  - UI can use proper progress bars

4. **No synthetic test case generator**
  - Currently manual CSV creation
  - Could add `scripts/generate_test_cases.py`

---

## Resources & References

### Implementation Plan
`~/.claude/plans/compiled-twirling-grove.md`

### Skill Code
`~/.claude/skills/evalcraft/` (all 12 files)

### Test Project
`~/Documents/eval_projects/fitness_coach_eval/`

### Eval Knowledge Base
`~/Documents/Eval Knowledge/` (3 research files)

### Similar Projects (Inspiration)
- Braintrust (eval platform) - https://braintrust.dev
- LangSmith (LangChain evals) - https://smith.langchain.com
- Promptfoo (open-source) - https://github.com/promptfoo/promptfoo

---

## Phase 2 Success Criteria

### MVP Web UI Complete When:
1. ✅ User can create rubric via web form
2. ✅ Visual rubric editor works (add/edit categories)
3. ✅ Can upload test data via drag-and-drop
4. ✅ Can run evaluation and see results
5. ✅ Results dashboard shows charts and traces
6. ✅ Can download generated code
7. ✅ Deployed and accessible via URL

### Portfolio-Ready When:
1. ✅ Clean, professional UI/UX
2. ✅ Demo video showing workflow
3. ✅ Comprehensive README with screenshots
4. ✅ Example use cases documented
5. ✅ Deployed with public URL
6. ✅ GitHub repo polished

---

## Next Session Checklist

**To resume Phase 2 work:**
- [ ] Read this resumption guide
- [ ] Review implementation plan: `~/.claude/plans/compiled-twirling-grove.md`
- [ ] Choose tech stack (Streamlit vs Next.js)
- [ ] Create new repo: `evalcraft-web`
- [ ] Copy scripts from `.claude/skills/evalcraft/scripts/` to backend
- [ ] Start with API routes (reuse existing Python scripts)
- [ ] Build wizard UI step-by-step
- [ ] Test with fitness coach example

**Reference materials ready:**
- All skill files preserved in `.claude/skills/evalcraft/`
- Test data in `~/Documents/eval_projects/fitness_coach_eval/`
- Eval knowledge in `~/Documents/Eval Knowledge/`

---

**Phase 1 is complete and validated. All code is preserved and ready for Phase 2.** 🚀
