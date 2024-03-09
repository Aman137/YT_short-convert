import streamlit as st
from dotenv import load_dotenv
load_dotenv() #load all the environment variable
import os
import google.generativeai as genai

from youtube_transcript_api import YouTubeTranscriptApi

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


prompt=("""You are youtube video summarizer.You will be taking the transcript text and summarize
the entire video and providing the important summary in points within 150 words. Please provide
the summary of the text given here:
        """)
#getting the transcript data from Yt video
def extract_transcript_details(youtube_video_url):
    try:
       video_id=youtube_video_url.split("=")[1]

       transcript_text = YouTubeTranscriptApi.get_transcript(video_id)

       transcript =""
       for i in transcript_text:
           transcript += " "+i["text"]

       return transcript
    except Exception as e:
        raise e
#getting the summary based on prompt from google gemini pro

# Function to generate summary based on the transcript using Google Gemini Pro
def generate_gemini_content(transcript_text):
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt + transcript_text)  # Fix the typo here
    return response.text


st.title("youtube Transcript to details note in-short")
youtube_link = st.text_input("Enter Y0utube video link:-")

if youtube_link:
    video_id= youtube_link.split("=")[1]
    st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", use_column_width=True)

if st.button("get deep notes"):
    transcript_text = extract_transcript_details(youtube_link)

    if transcript_text:
        summary = generate_gemini_content(transcript_text)
        st.markdown("## Detailed Notes:")
        st.write(summary)



