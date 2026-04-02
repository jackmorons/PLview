# PLview
Powerlifting data visualization tool

Main structure of the project:

- streamlit_app.py: main streamlit application

- home_page.py: home page of the application
- athlete_page.py: athlete page of the application
- record_page.py: record page of the application
- tools_page.py: tools page of the application
- info_page.py: info page of the application



possible tools:

- in records page:
    ✅ link the athletes to their athlete page

- in athlete page:
    ✅ radar plot showing the contribution of each lift to the total, showing the relative strength in each lift, and maybe a comparison with the record holders in the same cathegory or the average in the cathegory
    ✅ add a star on the timeline graph showing the prs
    ✅ gauge bar showing how strong you are within your cathegory, comparing your lifts to the average and the best in your cathegory

- in tools page:
    ------ create a tool to show where to move in the weight cathegories, showing similar weight athletes and a heatmap of their lifts - maybe showing where others sit within a specified weight range, or where the athlete would sit when cutting weight
    ------ create a tool to compare the performance of two athletes, showing their lifts and a comparison of their prs
    ------ trend calculator, given an expected 3rd lift calculate the first two based on successful trends in the same cathegory
    ------ pattern discoverer, what makes a strong lifter? mostly scatter plots of various + relative lifts correlation, showing the correlation between the lifts in the same cathegory (scatter squat vs bench, squat vs deadlift, bench vs deadlift) + age vs total, showing the correlation between age and total in the same cathegory
    ------ find your twin!!, find the athlete with the most similar performance to yours
    ------ average total by country (plotted on a map - maybe using geopandas)
    ------ freak finder - search for outliers, any athlete that is an outlier in any metric, far from the average, maybe combining an heatmap with a scatter plot
    ✅ index and 1RM calculator, calculate your projected 1Rep Max using the O'Conner formula with RPE adjustment




    