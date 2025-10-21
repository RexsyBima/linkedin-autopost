import os
import re
from pprint import pprint as print
from typing import Any

import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from pydantic_ai import Agent, WebSearchTool

# from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.models.openai import OpenAIResponsesModel

# from pydantic_ai.providers.deepseek import DeepSeekProvider
from pydantic_ai.providers.openai import OpenAIProvider
from youtube_transcript_api import FetchedTranscript, YouTubeTranscriptApi

load_dotenv()
url = os.getenv("URL_TARGET")
password = os.getenv("PASSWORD")


def post_to_webpage(password, title, description, body):
    assert url is not None, (
        "Url is None, this one should be filled, this is personal use anyway, you wont know"
    )
    headers = {
        "accept": "*/*",
        "Content-Type": "application/json",
    }
    data = {
        "password": password,
        "title": title,
        "description": description,
        "body": body,
    }

    response = requests.post(url, headers=headers, json=data)
    print(response.status_code)
    print(response.text)  # or response.json() if response is JSON


ytt_api = YouTubeTranscriptApi()

# model = OpenAIChatModel(
#     "deepseek-chat",
#     provider=DeepSeekProvider(api_key=os.getenv("DEEPSEEK_API", "")),
# )
#
#
# model = OpenAIChatModel(
#     "gpt-5-mini",
# )

model = OpenAIResponsesModel(
    "gpt-5-mini", provider=OpenAIProvider(api_key=os.getenv("OPENAI_API", ""))
)

system_prompt = """You are an AI agent that will reiterate a transcript text from a youtube video that will be used for personal branding post in a place like linkedin. the expected ouput will be always in linkedin post like format. you also have a tool in disposal to search through the web. in order to reiterate the transcript text to a good article for personal branding, You, the AI Agent must follow these following principles:
1. for writing a good article: minimize your barrier to entry. Make the article easy for reader to be drawn in.
A large opening paragraph at the start of an article is a huge barrier to entry. reader has to wade through a large wall of text before determining if the article is really interesting and worth reading. This requires a large expenditure of effort. Most people won’t bother.
Keep your opening short and punchy. A one-sentence or two-sentence leading paragraph is an easy buy-in. You can skim it and read it in barely more time than it would take to scroll past. Start with something short and easy to engage with. Prove to your reader that you’re providing value, then ask them to expend effort.

2. for writing a good article: keep the paragraphs of the article short and the text visually appealing. In general, shorten everything. Short paragraphs,  are tantalizing, easy to read, have the pace into it, make the reader want more a read into it. 
Balance words with empty spaces — like the breaths between spoken sentences.
Note: short does not mean that the writing can't be stylistic and beautiful. Do not make the mistake that short must be bland. Short paragraph means strong and precise 
When you're brief, your words aren't simple and cheapened. They're potent. by short paragraph, put it at most between 2 to 5 sentences each paragraph


3. for writing a good article: give the meaningful substance. One of the worst things on any news feed is an article that says nothing and its shockingly common. So often people just write fluff. Often the empty articles are packaged up as something useful. There are enough "top five tips" and "productivity hacks" articles in the world to last me to eternity. Rarely do any of them contain anything useful. They're just abstractions — they have nothing of substance to say.
There are more shallow, surface-level blog posts on my radar in any given day than I care to count.
They're made of words, but there's no point and no meaning. It's content for the sake of having content.
Don't write content for the sake of writing content. Write content for the sake of conveying meaning and understanding. Tell your reader something. Imagine they ask "why?" in response, and then answer that question.
The world does not need more surface-level going-through-the-motions content. It needs content designed to teach, convey meaning, make people understand.

4. tell the reader a story. People love stories. It's one of the basic truths of humanity — we, humans always respond to a compelling story. Keep this knowledge in your toolbox!
One of the best ways to draw a reader into an article is to bring it to life with human interest. Capture their attention with a recounting of an event, the setting of a stage, the unfolding of a plot.
Stories are a brilliant way to open articles. They're equally brilliant ways to illustrate a point. They don't have to be excessive and garish to be effective. Tell me in your article about a specific tool you recommend using, and then tell me a story about how you used it yourself and what it did for you. Short, simple, to the point, but suddenly your article is human.
Avoid dry writing. In the content-oversaturated age of the internet, nobody's going to read something bland.

5. for writing a good article: show, then tell. Start by showing me your point in action, then explain to reader what it means and why it matters.
This is a rule for your overall structure. Present your ideas in the following order: illustration, explanation, understanding. Show it to me, then tell me what it is, then help me understand why it works and how to use it myself.
Any other order will bore your reader, and will likely make less sense.

the expected output will something like this for an example, its in Indonesian, but keep the output in English:
Dengan teknik ini, gw berhasil potong budget kantor tapi hasil RAG-nya tetap akurat dan kontekstual.

Seperti kita tahu, performa model RAG (Retrieval Augmented Generation) itu sangat bergantung sama kualitas model embedder yang dipakai. Semakin canggih embedder-nya, makin akurat hasil pencariannya tapi biayanya juga makin tinggi.

Masalahnya, waktu itu budget-nya terbatas banget, tapi atasan tetap minta hasil RAG yang akurat dan bisa menjawab secara detail.

Nah gw bingung dong harus gimana, akhirnya curhat lah sama gpt dan akhirnya nemu solusi ini.

Alih-alih pakai embedder berbayar, gw tetap pakai model embedder gratis, tapi gw ubah strateginya.

Akhirnya gw pakai sistem child–parent chunking dan metadata retrieval.

Di strategi child–parent chunking, dokumen panjang gw pecah jadi potongan kecil (child chunk) supaya model bisa fokus ke bagian-bagian penting tanpa kehilangan konteks besarnya. Tapi tiap potongan kecil itu tetap “nyambung” ke bagian induknya (parent chunk), jadi konteks utuhnya tetap terjaga. 

Efeknya, dokumen panjang tetap relevan, dan dokumen pendek nggak kalah bersaing saat pencarian dilakukan.

Lalu di sisi lain, gw tambahkan metadata retrieval.
 
Kalau biasanya sistem cuma nyari kecocokan teks, di sini gw tambahkan “lapisan konteks” lewat metadata seperti tanggal, kategori, sumber, atau lokasi informasi. Jadi bukan cuma isi teks yang dibandingkan, tapi juga karakteristik dan konteks dari setiap dokumen. 

Dengan begitu, hasil pencarian bukan hanya lebih relevan secara semantik, tapi juga lebih tepat guna misalnya, model bisa tahu bahwa yang dimaksud “laporan” adalah laporan keuangan 2024, bukan laporan kegiatan biasa.

Hasil akhirnya:
 1. Jawaban model tetap detail dan nyambung
 2. Biaya embedding bisa ditekan jauh banget
 3. Akurasi pencarian meningkat signifikan

Kalau ada teknik lain yang worth it atau lebih canggih dari ini tolong komen ya gess, udah berkali kali revisi karna terhalang budget dan hasilnya minta tetep bagus.
"""
agent = Agent(model, system_prompt=system_prompt, builtin_tools=[WebSearchTool()])
system_prompt2 = """you are ai agent that designed for summarizing an article user will be provided. the expected output will always be like the linkedin post style
You. Follow the five steps outlined below to write a good summary.
the expected output will be only the result of the summarized text, no need of preposition
Follow the five steps outlined below to write a good summary.

Step 1: Read the text
You should read the article more than once to make sure you’ve thoroughly understood it. It’s often effective to read in three stages:

Scan the article quickly to get a sense of its topic and overall shape.
Read the article carefully, highlighting important points and taking notes as you read.
Skim the article again to confirm you’ve understood the key points, and reread any particularly important or difficult passages.
step 2: Break the text down into sections
To make the text more manageable and understand its sub-points, break it down into smaller sections.
If the text is a scientific paper that follows a standard empirical structure, it is probably already organized into clearly marked sections, usually including an introduction, methods, results, and discussion.
Other types of articles may not be explicitly divided into sections. But most articles and essays will be structured around a series of sub-points or themes.
Step 3: Identify the key points in each section
Now it’s time go through each section and pick out its most important points. What does your reader need to know to understand the overall argument or conclusion of the article?
Keep in mind that a summary does not involve paraphrasing every single paragraph of the article. Your goal is to extract the essential points, leaving out anything that can be considered background information or supplementary detail.
In a scientific article, there are some easy questions you can ask to identify the key points in each part.
Step 4: Write the summary
Now that you know the key points that the article aims to communicate, you need to put them in your own words.
To avoid plagiarism and show you’ve understood the article, it’s essential to properly paraphrase the author’s ideas. Do not copy and paste parts of the article, not even just a sentence or two.
The best way to do this is to put the article aside and write out your own understanding of the author’s key points.


the expected output will something like this for an example, its in Indonesian, but keep the output in English:
Dengan teknik ini, gw berhasil potong budget kantor tapi hasil RAG-nya tetap akurat dan kontekstual.

Seperti kita tahu, performa model RAG (Retrieval Augmented Generation) itu sangat bergantung sama kualitas model embedder yang dipakai. Semakin canggih embedder-nya, makin akurat hasil pencariannya tapi biayanya juga makin tinggi.

Masalahnya, waktu itu budget-nya terbatas banget, tapi atasan tetap minta hasil RAG yang akurat dan bisa menjawab secara detail.

Nah gw bingung dong harus gimana, akhirnya curhat lah sama gpt dan akhirnya nemu solusi ini.

Alih-alih pakai embedder berbayar, gw tetap pakai model embedder gratis, tapi gw ubah strateginya.

Akhirnya gw pakai sistem child–parent chunking dan metadata retrieval.

Di strategi child–parent chunking, dokumen panjang gw pecah jadi potongan kecil (child chunk) supaya model bisa fokus ke bagian-bagian penting tanpa kehilangan konteks besarnya. Tapi tiap potongan kecil itu tetap “nyambung” ke bagian induknya (parent chunk), jadi konteks utuhnya tetap terjaga. 

Efeknya, dokumen panjang tetap relevan, dan dokumen pendek nggak kalah bersaing saat pencarian dilakukan.

Lalu di sisi lain, gw tambahkan metadata retrieval.
 
Kalau biasanya sistem cuma nyari kecocokan teks, di sini gw tambahkan “lapisan konteks” lewat metadata seperti tanggal, kategori, sumber, atau lokasi informasi. Jadi bukan cuma isi teks yang dibandingkan, tapi juga karakteristik dan konteks dari setiap dokumen. 

Dengan begitu, hasil pencarian bukan hanya lebih relevan secara semantik, tapi juga lebih tepat guna misalnya, model bisa tahu bahwa yang dimaksud “laporan” adalah laporan keuangan 2024, bukan laporan kegiatan biasa.

Hasil akhirnya:
 1. Jawaban model tetap detail dan nyambung
 2. Biaya embedding bisa ditekan jauh banget
 3. Akurasi pencarian meningkat signifikan

Kalau ada teknik lain yang worth it atau lebih canggih dari ini tolong komen ya gess, udah berkali kali revisi karna terhalang budget dan hasilnya minta tetep bagus.
"""


agent2 = Agent(model, system_prompt=system_prompt2)

agent3 = Agent(
    model, instructions="based on user article input, generate a title for it"
)
# result = agent.run_sync("hello world")

agent4 = Agent(
    model,
    instructions="based on user article input, make the text to be html compatible, make sure only generate the html of the body only",
)

agent5 = Agent(
    model,
    instructions="based on user article input, generate a short description for it, make sure its less than 200 characters, which mean probably only two to three sentences only",
)


def _get_youtube_id(url: str) -> str | None:
    """
    Extracts the video ID from a YouTube URL.

    Args:
        url (str): The YouTube video URL.

    Returns:
        str | None: The video ID if found, otherwise None.
    """
    pattern = r"(?:v=|\/)([0-9A-Za-z_-]{11}).*"
    match = re.search(pattern, url)
    return match.group(1) if match else None


def _get_youtube_full_text(transcript: FetchedTranscript) -> str:
    output = ""
    for t in transcript:
        output += t.text
    return output


def _get_userinfo(secret: str) -> tuple[dict[str, Any], str]:
    url = "https://api.linkedin.com/v2/userinfo"
    headers = {"Authorization": f"Bearer {secret}"}
    response_json = requests.get(url, headers=headers).json()
    return response_json, response_json["sub"]


def _register_media(profile_id: str, access_token: str):
    headers = {
        "Content-Type": "application/json",
        "X-Restli-Protocol-Version": "2.0.0",
        "Authorization": "Bearer " + access_token,
    }

    post_data = {
        "registerUploadRequest": {
            "recipes": ["urn:li:digitalmediaRecipe:feedshare-image"],
            "owner": "urn:li:person:" + profile_id,
            "serviceRelationships": [
                {
                    "relationshipType": "OWNER",
                    "identifier": "urn:li:userGeneratedContent",
                }
            ],
        }
    }
    url = "https://api.linkedin.com/v2/assets?action=registerUpload"
    response = requests.post(url, headers=headers, json=post_data)
    return response


def post_content_no_image(content: str, profile_id: str, access_token: str):
    url = "https://api.linkedin.com/v2/ugcPosts"

    headers = {
        "Content-Type": "application/json",
        "X-Restli-Protocol-Version": "2.0.0",
        "Authorization": "Bearer " + access_token,
    }
    post_data = {
        "author": "urn:li:person:" + profile_id,
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {"text": content},
                "shareMediaCategory": "NONE",
            }
        },
        "visibility": {"com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"},
    }

    response = requests.post(url, headers=headers, json=post_data)
    return response


def _post_content_image(
    content: str, profile_id: str, access_token: str, media_asset: str
):
    url = "https://api.linkedin.com/v2/ugcPosts"
    headers = {
        "Content-Type": "application/json",
        "X-Restli-Protocol-Version": "2.0.0",
        "Authorization": "Bearer " + access_token,
    }
    post_data = {
        "author": f"urn:li:person:{profile_id}",
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {"text": content},
                "shareMediaCategory": "IMAGE",
                "media": [
                    {
                        "status": "READY",
                        "description": {"text": "Center stage!"},
                        "media": media_asset,
                        "title": {"text": "LinkedIn Talent Connect 2021"},
                    }
                ],
            }
        },
        "visibility": {"com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"},
    }
    response = requests.post(url, headers=headers, json=post_data)
    return response


def post_personal_branding_with_image(
    image_path: str | None = None, content: str | None = None
):
    user_secret = os.getenv("USER_SECRET")
    if image_path is None or content is None or user_secret is None:
        raise Exception(
            "parameter of image_path and content must be filled bruh, also .env of USER_SECRET must be filled"
        )
    _, profile_id = _get_userinfo(user_secret)
    response = _register_media(profile_id, user_secret)
    asset = response.json()["value"]["asset"]
    url = response.json()["value"]["uploadMechanism"][
        "com.linkedin.digitalmedia.uploading.MediaUploadHttpRequest"
    ]["uploadUrl"]

    headers = {"Authorization": f"Bearer {os.getenv('USER_SECRET')}"}
    with open(image_path, "rb") as f:
        response = requests.post(url, headers=headers, data=f)
    response = _post_content_image(
        content=content,
        profile_id=profile_id,
        access_token=user_secret,
        media_asset=asset,
    )

    return response


def html_to_text_with_lists(soup: BeautifulSoup):
    lines = []

    def walk(node, indent=0, ol_level=0):
        if node.name == "ul":
            for li in node.find_all("li", recursive=False):
                lines.append("  " * indent + "* " + walk(li, indent + 1))
        elif node.name == "ol":
            i = 1
            for li in node.find_all("li", recursive=False):
                lines.append("  " * indent + f"{i}. " + walk(li, indent + 1))
                i += 1
        elif node.name == "li":
            # If li has nested ul/ol, handle separately
            text = node.get_text(" ", strip=True)
            sublists = node.find_all(["ul", "ol"], recursive=False)
            return text if not sublists else text
        else:
            # For headings, paragraphs, etc.
            if node.string:
                return node.string.strip()
            else:
                return " ".join(
                    child.get_text(" ", strip=True) for child in node.children if child
                )

    for child in soup.children:
        txt = walk(child)
        if txt:
            if isinstance(txt, str):
                lines.append(txt)

    return "\n".join(lines)


def get_youtube_text(url: str) -> str:
    video_id = _get_youtube_id(url)
    assert video_id is not None, "Video ID incorrect"
    transcript = _get_youtube_full_text(ytt_api.fetch(video_id))
    return transcript


def get_ai_do_it(url: str, context: str):
    video_id = _get_youtube_id(url)
    assert video_id is not None, "Video ID incorrect"
    transcript = _get_youtube_full_text(ytt_api.fetch(video_id))
    output = agent.run_sync(transcript)
    filename = agent3.run_sync(transcript)
    with open(filename.output + ".txt", "w") as f:
        f.write(output.output)
    if len(output.output) > 3000:
        output = agent2.run_sync(output.output)
        with open(filename.output + "-summarized.txt", "w") as f:
            f.write(output.output)
    if len(output.output) > 3000:
        raise Exception(
            f"Error, fail, the output of the llm has more than 3000 characters, its output is {output.output}"
        )


def list_txt_files() -> list[str]:
    """List all .txt files in a directory (non-recursive) and return their paths."""
    directory = os.getcwd()
    txt_files = []
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            txt_files.append(filename)
    return txt_files


def list_txt_files_full_path() -> list[str]:
    """List all .txt files in a directory (non-recursive) and return their paths."""
    directory = os.getcwd()
    txt_files = []
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            full_path = os.path.join(directory, filename)
            txt_files.append(os.path.abspath(full_path))
    return txt_files


def get_html_txt(url: str):
    response = requests.get(url).text
    soup = BeautifulSoup(response, "html.parser")
    body = soup.body
    assert body is not None, "body tag is None, canceling"
    result = body.get_text(strip=True)
    return result


def get_ai_do_it_html(text: str):
    output = agent.run_sync(text)
    filename = agent3.run_sync(text)
    with open(filename.output + ".txt", "w") as f:
        f.write(output.output)
    if len(output.output) > 3000:
        output = agent2.run_sync(output.output)
        with open(filename.output + "-summarized.txt", "w") as f:
            f.write(output.output)
    if len(output.output) > 3000:
        raise Exception(
            f"Error, fail, the output of the llm has more than 3000 characters, its output is {output.output}"
        )


if __name__ == "__main__":
    print("1. generate personal branding, based on youtube link")
    print(
        "2. generate personal branding, based on url html link, (this feauture is wip, especially for js heavy website)"
    )
    print(
        "3. choose personal branding and post it to linkedin (i assume you will do the manual checking urself, fix text error, and adjust to your style urself)"
    )
    print(
        "4. choose personal branding and post it to linkedin, with image post (i assume you will do the manual checking urself, fix text error, and adjust to your style urself)"
    )
    print("5. post a txt file to my webpage (this is personal use only, you wont know)")
    menu_choice = int(input("please put ur menu action here"))
    if menu_choice == 1:
        url = input("please put the url here: ")
        context = input(
            "please add more context if u want, leave it empty if u want none: "
        )
        get_ai_do_it(url, context)
        exit()
    elif menu_choice == 2:
        url = input("please put the url here: ")
        text = get_html_txt(url)
        get_ai_do_it_html(text)
        exit()
    elif menu_choice == 3:
        txt = list_txt_files_full_path()
        file_names = list_txt_files()
        for i, t in enumerate(file_names):
            print(f"{i}. {t}")
        choice = int(input("please input which text you want to generate"))
        choice = txt[choice]
        print(f"are you sure this is ur choice : {choice}")
        ... if input("press 1 to continue, else to exit") == "1" else exit(
            "Canceling..."
        )
        # post_personal_branding_with_image("./tes.png", content=output)
        user_secret = os.getenv("USER_SECRET")
        assert user_secret is not None, ""
        _, profile_id = _get_userinfo(user_secret)
        with open(choice, "r") as f:
            content = f.read()
        if len(content) > 3000:
            raise Exception(
                f"Your content is too long, wont be able to publish it into linkedin, your length content is at {len(content)}, required content length (character) to be less than 3000"
            )
        response = post_content_no_image(
            content=content,
            access_token=user_secret,
            profile_id=profile_id,
        )
        if response.status_code == 201:
            os.rename(choice, choice + ".completed")
        print(response.content)
        print(response.json())
        print(response)
    elif menu_choice == 4:
        txt = list_txt_files_full_path()
        file_names = list_txt_files()
        for i, t in enumerate(file_names):
            print(f"{i}. {t}")
        choice = int(input("please input which text you want to generate"))
        choice = txt[choice]
        print(f"are you sure this is ur choice : {choice}")
        ... if input("press 1 to continue, else to exit") == "1" else exit(
            "Canceling..."
        )
        user_secret = os.getenv("USER_SECRET")
        assert user_secret is not None, ""
        _, profile_id = _get_userinfo(user_secret)
        with open(choice, "r") as f:
            content = f.read()
        if len(content) > 3000:
            raise Exception(
                f"Your content is too long, wont be able to publish it into linkedin, your length content is at {len(content)}, required content length (character) to be less than 3000"
            )

        img_choice = input(
            "please input the image path in current working directory you want to use: "
        )
        response = post_personal_branding_with_image("./" + img_choice, content=content)
        if response.status_code == 201:
            os.rename(choice, choice + ".completed")
        print(response.content)
        print(response.json())
        print(response)
    elif menu_choice == 5:
        txt = list_txt_files_full_path()
        filename = list_txt_files()
        for i, t in enumerate(txt):
            print(f"{i}. {t}")
        choice = int(input("please input which text you want to generate"))
        text_input = txt[choice]
        text_file = filename[choice]
        print(f"are you sure this is ur choice : {choice}")
        ... if input("press 1 to continue, else to exit") == "1" else exit(
            "Canceling..."
        )
        with open(text_input, "r") as f:
            content = f.read()

        result = agent4.run_sync(content).output
        description_result = agent5.run_sync(content).output
        post_to_webpage(password, text_file, description_result, result)
