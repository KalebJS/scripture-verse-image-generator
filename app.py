import os
import sqlite3

import pandas as pd
import streamlit as st

from source import OpenAIService

gpt = OpenAIService(os.environ["OPENAI_API_KEY"])

conn = sqlite3.connect("kjv.sqlite")
query = (
    "SELECT verses.id, books.name, verses.chapter, verses.verse FROM verses INNER JOIN books ON verses.book = books.id;"
)
df = pd.read_sql_query(query, conn)

book_options = df["name"].unique()
selected_book = st.selectbox("Select Book", book_options)
filtered_df = df[df["name"] == selected_book]

max_chapter = filtered_df["chapter"].max()
chapter_number = st.number_input("Enter Chapter Number", min_value=1, max_value=max_chapter, value=1, step=1)

max_verse = filtered_df[filtered_df["chapter"] == chapter_number]["verse"].max()
verse_number = st.number_input("Enter Verse Number", min_value=1, max_value=max_verse, value=1, step=1)
verse_id = filtered_df[(filtered_df["chapter"] == chapter_number) & (filtered_df["verse"] == verse_number)]["id"].iloc[
    0
]
verse_id = int(verse_id)

query = "SELECT id, verse, text FROM verses WHERE id IN ({verse_list})".format(
    verse_list=", ".join(map(str, range(verse_id - 2, verse_id + 3)))
)
verse_context = pd.read_sql_query(query, conn)
verse_context.set_index("id", inplace=True)
st.divider()
for _, verse in verse_context.iterrows():
    if verse.name == verse_id:
        st.write(str(verse.verse), f"__{verse.text}__")
    else:
        st.write(str(verse.verse), verse.text)
st.divider()

if st.button("Generate"):
    image_generation_prompt = gpt.create_image_prompt(
        selected_book, chapter_number, verse_number, verse_context.loc[verse_id].text, "\n".join(verse_context.text)
    )
    st.write(image_generation_prompt)
    image_paths = gpt.generate_images(image_generation_prompt)
    for fp in image_paths:
        st.image(str(fp))
