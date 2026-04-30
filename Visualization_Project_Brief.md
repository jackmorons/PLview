# Visualization Project Brief: PLview

## 1. Topic
The project domain is sports analytics, specifically focused on powerlifting. It centers on visualizing athlete performance, competition history, strength distributions, and benchmarking metrics (such as Dots and Wilks scores) across various demographic and physical categories including age, gender, weight class, and equipment type.

## 2. Motivating Curiosity
The visualization is driven by the desire to contextualize individual physical strength within a global, historical landscape. Powerlifting is inherently numbers-driven, yet raw numbers lack meaning without context. The underlying curiosity is to understand: "How strong is an athlete relative to their true peers?", "What physical or demographic factors correlate most with elite performance?", and "What historical trends can predict or optimize future competition outcomes?" 

## 3. Specific Question
This curiosity translates into several precise, actionable visualization questions:
* How does an athlete's individual performance profile (Squat, Bench, Deadlift, Total) benchmark against the statistical average and all-time records of their exact demographic category?
* Is there a mathematical and competitive advantage for an athlete to change their body weight to compete in a different weight class?
* What are the historical success patterns for attempt selection in specific categories, and how can they inform an athlete's strategy for achieving a target third attempt?
* How do different powerlifting variables (e.g., bodyweight, age, specific lifts) correlate across the broader population?

## 4. Stakeholder / Customer
The primary stakeholders are the professors and evaluators of the university Data Visualization course for which this project was developed; they will evaluate the project based on data handling, visual encoding choices, and analytical coherence. The secondary, functional "customers" are powerlifting coaches and athletes. Their interest lies in actionable insights, intuitive interfaces, and reliable data modeling that can inform training and competition strategies.

## 5. Audience
The target audience consists of powerlifting athletes, coaches, and strength sports enthusiasts. 
* **Domain Knowledge:** High. The audience is fluent in powerlifting terminology, including coefficients (Dots, Wilks), equipment categories (Raw, Wraps, Multi-ply), and competition rules.
* **Visualization Literacy:** Moderate. While they understand basic charts, they are likely unaccustomed to reading multi-dimensional or statistical visualizations like density heatmaps, correlation matrices, or multi-axis radar charts.
* **Motivations:** They are driven by competition, self-improvement, and strategic planning. They want to find advantages, compare themselves to rivals, and understand their standing in the "ocean" of lifters.
* **Interpretation Needs:** The audience requires contextual helpers to accurately interpret statistical concepts (e.g., Pearson coefficients, percentiles) without feeling overwhelmed.

## 6. Decision / Action
The visualizations are designed to support the following actions and behaviors:
* **Strategic Planning:** Deciding whether to move up or down a weight class based on projected percentile rankings and strength-retention models.
* **Competition Execution:** Selecting safe and optimal competition attempts based on historical 3-for-3 success trends within an athlete's specific category.
* **Training Focus:** Identifying individual physiological weaknesses (e.g., a relatively weak bench press compared to category averages) through radar charts, thereby directly informing the programming of future training cycles.

## 7. Data
* **Datasets:** The project uses a curated, split subset of the OpenPowerlifting database (separated into male and female datasets to optimize memory usage).
* **Variables:** Includes categorical data (Name, Equipment, AgeClass, Federation) and quantitative data (BodyweightKg, Best3SquatKg, Best3BenchKg, Best3DeadliftKg, TotalKg, Dots, and individual attempts).
* **Granularity:** The data is granular down to the level of individual competition entries, encompassing over 120,000 records.
* **Data Quality Considerations:** Anomalies (such as 0kg bodyweight outliers) and single-lift competitions have been cleaned out to ensure statistical averages represent full powerlifting meets. Failed attempts are captured as negative values to allow for accurate progression and trend tracking.
* **Limitations:** The dataset relies exclusively on historical, public competition data. It does not account for gym lifts, training age, or injuries, meaning predictive tools operate under the assumption of normal competition conditions. 

## 8. Constraints
* **Platform:** Built on Streamlit, which imposes architectural constraints on UI layout, state management, and interaction design. The application must perform fluidly in a browser while filtering tens of thousands of rows of data using Pandas in the backend.
* **Audience Limitations:** The moderate statistical literacy of the audience forces the design to avoid overly academic presentations unless accompanied by explicit guides or gamified wrappers.
* **Time and Skills:** As a university project developed by a small student team, time constraints limit the implementation of complex backend infrastructure or real-time database syncing, necessitating the use of static CSV files loaded into session state memory.
* **Screen Space:** Rendering complex comparison tools side-by-side requires careful grid management to prevent mobile or small-screen overlap.

## 9. Freedoms
* **Visual Style:** Complete freedom over the aesthetic tone. The developers utilized custom CSS injection and Plotly's flexible templating (`plotly_dark`) to override default Streamlit styles, creating a bespoke UI.
* **Tooling and Narrative:** Freedom to experiment with non-traditional, engaging analytical narratives. This allows for the creation of gamified tools like the "1v1 Strength Comparison," "Find Your Powerlifting Twin," and the "Weight Class Evaluator," transforming dry data exploration into an engaging experience.
* **Chart Selection:** Freedom to use advanced charting libraries (Plotly) to create interactive density heatmaps, radar charts, and gauges that go beyond standard reporting.

## 10. Consumption Setting
The visualization will primarily be consumed on desktop or laptop browsers, likely during periods of training analysis or competition planning (e.g., a coach reviewing data at a desk, or an athlete checking stats after a training block). The setting is analytical but informal. It is not designed for dynamic, real-time use on the platform during a high-stress competition, but rather for deliberate, pre-competition strategy sessions or post-competition reflection.

## 11. Medium
The deliverable is an interactive, multi-page web application.
* **Format:** Digital, highly interactive dashboard.
* **Navigation:** Structured into specific modular views (Home, Athletes, Records, Tools, Info) to manage complexity and prevent cognitive overload.
* **Screen Constraints:** Optimized for wide screens (`layout="wide"`) to accommodate complex, side-by-side comparative visualizations (like dual radar charts and data tables).
* **Update Frequency:** Static relative to the provided CSV datasets, requiring manual repository updates to refresh the OpenPowerlifting data.

## 12. Tone
The appropriate tone is a **Hybrid** of precision and emotional engagement.
* **Analytical Precision:** The tools are mathematically rigorous, calculating exact percentiles, Dots scores, and standard deviations to provide genuine, data-backed insights.
* **Emotional Impact:** The UI leverages a dark, modern "sports-broadcast" aesthetic. The use of emojis, competitive framing ("1v1 Battle", "Freak Finder", "Trust Me Bro Speculator"), and gamified metrics (percentile gauges, radar overlays) creates an emotional resonance that matches the competitive, adrenaline-driven nature of powerlifters. 

## 13. Experience
The experience is primarily **Exploratory**, heavily augmented by **Explanatory** features.
* **Exploratory:** Users are actively driving the dashboard. They input their own weight, search for specific rivals, filter distributions by equipment, and simulate weight cuts. The visualizations dynamically update in response to their specific queries.
* **Explanatory:** Because the tools generate complex statistical outputs, the interface wraps them in explanatory context. The "Chart Reading 101" section, tooltips, and contextual warnings (e.g., low sample size alerts) guide the user through the data discovery process, ensuring the user acts as an informed participant.

## 14. Success Criteria
The project's effectiveness should be evaluated on the following outcomes:
* **Academic Success:** Satisfying the requirements of the Data Visualization course through appropriate visual encoding, data cleaning, and narrative flow.
* **Communication Effectiveness:** The ability of users to correctly interpret complex charts (like the density heatmap or radar chart) without confusion, aided by the UI's explanatory elements.
* **Operational Usefulness:** The degree to which athletes and coaches find the strategic tools (Weight Class Evaluator, Entry Calculator) logically sound and practically useful for real-world planning.
* **Engagement:** The perceived "wow factor" and user retention, driven by the gamified tone, fast search, and sleek dark-mode aesthetics.

---

## FINAL SECTION — SYNTHESIS
The overall visualization strategy for PLview is to democratize complex sports analytics by wrapping rigorous statistical data in an engaging, gamified, and highly interactive interface. It acknowledges that while powerlifters are obsessed with numbers, they respond best to visual storytelling that frames data in the context of competition, benchmarking, and strategic advantage. 

By balancing the technical constraints of the Streamlit platform with creative freedoms in CSS styling and Plotly interactivity, the project transforms a massive, static CSV database into a dynamic coaching assistant. The modular architecture prevents information overload, separating simple profile lookups from deep statistical modeling. 

The most important design implication emerging from this brief is the necessity of "guided exploration." Because the audience's domain knowledge exceeds their statistical literacy, every complex chart—from correlation matrices to density heatmaps—must be accompanied by clear explanations, intuitive tooltips, and interactive filtering. This approach ensures the visualization remains an empowering, accessible tool for athletes rather than an intimidating academic exercise.
