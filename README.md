# Inverse Dynamic Model

## Project Overview
This project is focused on developing an Inverse Dynamic Model capable of annotating video frames. The primary aim is to extract and annotate actions from videos of people using software to accomplish tasks. This involves scraping videos, processing frames, and utilizing both Vision-Language Models (VLMs) and Language Learning Models (LLMs) for annotation.

### Key Objectives
- **Video Retrieval:** Collect videos of individuals using software to perform tasks.
- **Action Extraction:** Use VLM prompts to extract actions from specific frames in both past and future contexts.

## Pipeline
Our project pipeline consists of the following steps:

1. **Video Scraping:**
   - **Script:** `youtube_scraper.py`
   - **Details:** Scrapes approximately 40 videos from YouTube, each not exceeding 4 minutes in length.

2. **Frame Processing:**
   - **Script:** `video_frame_creator.py`
   - **Details:** Splits each video into frames at 2-second intervals, resulting in around 3000 frames.

3. **Annotation:**
   - **Script:** `pipeline.py`
   - **Details:** Utilizes VLM and LLM models to annotate frames based on predefined prompts and an output grammar.


## Requirements
To run the scripts and use the models effectively, ensure you have the following:

- Python 3.8 or newer
- Libraries: OpenCV for video processing, Transformers

## For running scripts
Clone this repository and install the required Python libraries:

```bash
git clone https://github.com/A-Mahla/Inverse-dynamic-model.git
cd Inverse-dynamic-model
pip install -r requirements.txt
```

## Contributing
Contributions to this project are welcome. Please fork the repository and submit pull requests for any enhancements.
