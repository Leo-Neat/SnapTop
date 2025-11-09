# Copilot Instructions for AI Agents

## Project Overview
This is a multi-agent meal planning system using LangGraph, LangChain, and Python. It generates personalized weekly meal plans, recipes, nutritional analysis, and shopping lists. The backend exposes a gRPC API for a web frontend, with all persistent data stored in Google Cloud BigQuery.

## Architecture & Workflow
- **Agents:**
  - **Meal Planner:** Proposes meal ideas based on user profile and requirements. Human-in-the-loop approval.
  - **Nutritionist:** Allocates macro targets per meal, ensuring weekly goals are met.
  - **Chef:** Generates recipes using web search and Nutrition API, iterates per meal.
  - **Validator:** Checks recipes against user constraints, equipment, macros, and clarity. Feedback loops to Chef.
- **State Management:**
  - Use LangGraph to maintain state across workflow stages and human checkpoints.
  - Store intermediate agent outputs for rollback and debugging.
- **API Endpoints (gRPC):**
  - `GenerateWeeklyMeals`, `RegenerateRecipe`, `ModifyRecipe`, `GetShoppingList`.
  - All endpoints stream progress and support human-in-the-loop modifications.

## Data & Protocols
- **Protocol Buffers:**
  - Key messages: `UserProfile`, `Recipe`, `ShoppingList` (see README for schema details).
- **BigQuery Tables:**
  - `users`, `recipes` (with version history), `meal_plans`, `agent_logs`.
- **External APIs:**
  - Nutrition API: https://api-ninjas.com/api/nutrition
  - Web search for recipe research (track citations).

## Developer Workflows
- **Build/Run:**
  - Use Python (uv) for package management.
  - gRPC for API communication; Protocol Buffers for serialization.
  - Deploy and store data on Google Cloud Platform.
- **Testing/Debugging:**
  - Track agent decisions in `agent_logs` for debugging.
  - Validation failures must return actionable feedback.
  - Implement retry logic for LLM and external API calls.

## Project-Specific Conventions
- **Human-in-the-loop:**
  - Users can approve, modify, or regenerate meal plans/recipes at any stage.
  - Failed validation loops back to Chef agent with feedback.
- **Recipe Generation:**
  - All recipes must cite sources and match user dietary/equipment constraints.
  - Macro targets must be met within tolerance.
- **Security:**
  - Encrypt user data at rest (BigQuery).
  - Use TLS for gRPC.
  - Handle PII per dietary/health compliance.

## Key Files & Directories
- `README.md`: Full technical specification and protobuf schemas.
- `.github/copilot-instructions.md`: AI agent guidelines (this file).
- BigQuery tables: `users`, `recipes`, `meal_plans`, `agent_logs`.

## Example Patterns
- **Agent Pipeline:**
  - `PLANNING → Human approval → NUTRITION_ALLOCATION → RECIPE_GENERATION → VALIDATION`
  - Validation failures: `VALIDATION → RECIPE_GENERATION`
- **API Usage:**
  - `GenerateWeeklyMeals(UserProfile, WeeklyMealRequest) → WeeklyMealPlan`
  - `RegenerateRecipe(RecipeId, Reason) → Recipe`
  - `ModifyRecipe(RecipeId, Instructions) → Recipe`
  - `GetShoppingList(WeeklyMealPlanId, Pantry) → ShoppingList`

---

**Feedback requested:** Please review and suggest additions or clarifications for any unclear or incomplete sections.