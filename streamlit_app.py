"""KNM HORIZON · 56-day A2 Dutch integration knowledge studio.

Self-contained Streamlit app. Course facts and book chapter organisation follow the user's
uploaded TaalCompleet KNM text. Long explanations, examples and quiz questions are
original pedagogical supplements. It is not the official DUO test.
"""
from __future__ import annotations
import html
import json
import math
import csv
import io
from collections import Counter
from pathlib import Path
from datetime import datetime, timezone
import streamlit as st
from study_depth import DEEP, CONCEPT_LENS, SENTENCE_STARTERS

BASE=Path(__file__).resolve().parent
DATA=json.loads((BASE/'course_content.json').read_text(encoding='utf-8'))
PAGES=['🌅  Home','🗓️  56-day roadmap','📚  Detailed lessons','🧠  Visual memory','📝  Practice exams','📊  My progress','ℹ️  About the course']
THEMES={t['id']:t for t in DATA['themes']}

st.set_page_config(page_title='KNM HORIZON | 56-day Dutch Life',page_icon='🌅',layout='wide',initial_sidebar_state='expanded',menu_items={'About':'Original bilingual A2 Dutch course inspired by the uploaded TaalCompleet KNM textbook.'})

CSS='''
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&family=Outfit:wght@400;500;600;700;800;900&display=swap');
:root{--ink:#152331;--navy:#101f35;--blue:#4355a0;--lilac:#a69de3;--citrus:#edfdab;--border:#dee4ee;--muted:#657285}
.stApp{background:#F5F7FB;color:var(--ink)}html,body,[class*="css"],p,li{font-family:'DM Sans',system-ui,sans-serif}
h1,h2,h3{font-family:'Outfit',system-ui,sans-serif!important;color:#152331!important;letter-spacing:-.038em}
[data-testid="stSidebar"]{background:#F0F2FA;border-right:1px solid #DCE2F1}
[data-testid="stSidebar"] hr{border-color:#D7DDEA}
[data-testid="stSidebar"] label{font-weight:700;color:#3C456A}
[data-testid="stHeader"]{background:transparent}
.block-container{max-width:1400px;padding-top:2rem;padding-bottom:5rem}
.stButton>button[kind="primary"]{background:#465AA8;border-color:#465AA8;color:white;border-radius:13px;font-weight:800;padding:.63rem 1.07rem}
.stButton>button[kind="secondary"]{border-radius:13px;border-color:#D9E0ED;background:#fff;color:#263657;font-weight:700;padding:.54rem .9rem}
.stButton>button:hover{border-color:#596BDD!important;color:#596BDD!important}
[data-testid="stMetric"]{background:white;padding:19px 19px 14px;border:1px solid #E0E5EF;border-radius:17px}
[data-testid="stMetricLabel"]{font-size:.9rem;color:#647083}
[data-testid="stMetricValue"]{font-weight:900;color:#202E4D}
[data-testid="stExpander"]{border:1px solid #DDE3EF;background:white;border-radius:17px;overflow:hidden}
[data-testid="stRadio"] label, [data-testid="stCheckbox"] label{font-size:.96rem}
[data-testid="stProgress"]>div>div{background:#9B95E8!important}
.stTabs [data-baseweb="tab-list"]{gap:8px}
.stTabs [data-baseweb="tab"]{background:#E8EDFC;border-radius:11px;padding:7px 15px}
.horizon-logo{font-family:Outfit,system-ui;font-size:23px;font-weight:900;letter-spacing:-.065em;color:#1E3155}
.horizon-logo em{color:#6272C4;font-style:normal}
.sidebar-tiny{font-size:11px;color:#64769A;letter-spacing:.13em;font-weight:800;text-transform:uppercase}
.eyebrow{color:#7072BA;font-size:12px;font-weight:900;letter-spacing:.18em;text-transform:uppercase;margin-bottom:11px}
.hero{border-radius:26px;padding:36px 43px;color:white;background:radial-gradient(circle at 87% 9%,#58658A 0,#2F437D 24%,transparent 43%),linear-gradient(120deg,#101F34,#293F78 69%,#4059A4);position:relative;overflow:hidden;margin-bottom:22px}
.hero:before{content:'◌';position:absolute;right:27px;top:-122px;font-size:460px;opacity:.11;line-height:1;font-family:Georgia,serif}
.hero h1{font-size:clamp(35px,4.5vw,62px);margin:0 0 14px;color:white!important;line-height:1.09;max-width:960px}
.hero p{font-size:17px;color:#DAE4FC;max-width:810px;line-height:1.65;margin:8px 0}
.hero .eyebrow{color:#E7F69E}
.hero .strip{display:flex;gap:10px;flex-wrap:wrap;margin-top:24px}.hero .strip span{padding:7px 12px;border-radius:99px;background:#ffffff1d;border:1px solid #ffffff38;font-size:12px;font-weight:800}
.section-tag{font-size:12px;text-transform:uppercase;letter-spacing:.15em;color:#646CB3;font-weight:900;margin-top:8px;margin-bottom:6px}
.lesson-reading{background:#EFF2FF;border-left:5px solid #938EE7;border-radius:16px;padding:22px 25px;margin:12px 0 16px;line-height:1.9;color:#243656;font-size:18px}
.softbox{background:#fff;border:1px solid #E1E5EF;border-radius:19px;padding:22px 24px;margin:12px 0 21px;box-shadow:0 6px 20px #27356906}
.softbox h3{margin:0 0 11px;font-size:20px}
.captionline{font-size:13px;color:#67778A;line-height:1.6}
.memory-ribbon{background:#142841;color:#E6F3FF;padding:21px;border-radius:18px;margin:13px 0;font-size:20px;font-weight:800;line-height:1.6}
.memory-ribbon .mini{color:#C5D6F6;font-size:11px;letter-spacing:.13em;text-transform:uppercase;display:block;margin-bottom:7px}
.topic-pill{display:inline-flex;background:#E7EAFB;color:#4E5D9C;font-size:12px;border-radius:99px;padding:8px 12px;font-weight:800;margin-right:7px;margin-bottom:7px}
.week-banner{display:flex;align-items:center;gap:17px;background:#ECEFFA;border:1px solid #D7DFF4;border-radius:17px;padding:19px;margin-bottom:18px}
.week-banner .badge{width:48px;height:48px;display:flex;align-items:center;justify-content:center;background:#5466BA;color:white;border-radius:14px;font-size:22px;font-weight:900}
.step-line{display:flex;gap:12px;align-items:flex-start;margin:11px 0}.step-line .num{background:#E6EBFF;color:#4A5A9C;width:27px;min-width:27px;height:27px;display:flex;justify-content:center;align-items:center;border-radius:50%;font-weight:900;font-size:13px}
.mem-chain{display:flex;gap:11px;margin:15px 0 22px;flex-wrap:wrap}.mem-node{background:#F0F2FF;border:1px solid #DAE0F8;border-radius:17px;flex:1;min-width:125px;padding:20px 11px;text-align:center}.mem-node .symbol{font-size:31px;display:block;margin-bottom:10px}.mem-node b{font-size:13px;color:#32426D}
.callout{background:#FFF5E4;border:1px solid #F1D6B2;padding:16px 20px;border-radius:17px;color:#6B502D}
.hints{background:#E5EDFF;border-radius:14px;padding:14px 16px;color:#3A4D75;font-size:14px}
.vocab-item{background:#fff;border:1px solid #DAE2EF;border-radius:15px;padding:17px 19px;min-height:87px;margin-bottom:9px}.vocab-item .nl{font-size:18px;font-weight:900;color:#445AA1}.vocab-item .en{font-size:13px;color:#67768A;margin-top:6px}
.hero-small{font-size:14px;color:#53648B}
.results-big{background:#182F58;color:white;border-radius:24px;padding:30px;text-align:center}.results-big b{font-size:58px;line-height:1.2}
.book-foot{font-size:12px;color:#6D798C;padding:11px 0}
@media(max-width:780px){.hero{padding:27px 23px;border-radius:20px}.hero:before{font-size:220px;right:-15px;top:-45px}.hero h1{font-size:35px}.block-container{padding-top:1.2rem}.lesson-reading{font-size:17px;padding:18px 19px}.softbox{padding:18px}}
</style>
'''
st.markdown(CSS,unsafe_allow_html=True)

def E(s):return html.escape(str(s))
def card(body,title=None):
    head=f'<h3>{E(title)}</h3>' if title else ''
    st.markdown(f'<div class="softbox">{head}{body}</div>',unsafe_allow_html=True)

def memory_chain(text):
    # visually memorable but preserve the actual mnemonic exactly
    st.markdown(f'<div class="memory-ribbon"><span class="mini">✳ VISUAL MEMORY CUE</span>{E(text)}</div>',unsafe_allow_html=True)

def speak_prompt(message):
    st.caption('🔊 Speak the Dutch text aloud twice. Pronunciation practice is oral; this app does not record or score your speech.')

def init():
    ss=st.session_state
    for k,v in {'page':PAGES[0],'day':1,'done':[],'answers':{},'graded':{},'review_notes':{},'confidence':{},'card_idx':{},'flip':False,'qposition':{},'qday':50,'book_filter':'All themes'}.items():
        if k not in ss: ss[k]=v
init()

def go(page,day=None):
    if day is not None:st.session_state.day=day
    st.session_state.page=page
    st.rerun()

def get_day(day):return DATA['days'][day-1]
def get_week(day):return (day-1)//7+1

def sidebar():
    with st.sidebar:
        st.markdown('<div class="horizon-logo">🌅 KNM <em>HORIZON</em></div><div class="sidebar-tiny">56 DAYS · DUTCH LIFE MADE CLEAR</div>',unsafe_allow_html=True)
        st.markdown('---')
        for p in PAGES:
            sel=st.session_state.page==p
            if st.button(p,key='menu_'+p,type='primary' if sel else 'secondary',use_container_width=True):go(p)
        st.divider()
        st.markdown('**Jump to a study day**')
        day=st.selectbox('Choose day 1–56',range(1,57),index=st.session_state.day-1,format_func=lambda d:f'Day {d:02d} · W{get_week(d)} · {get_day(d)["title"]}',label_visibility='collapsed')
        if st.button('Open this lesson ↗',use_container_width=True):go(PAGES[2],day)
        st.divider()
        st.caption(f'**{len(st.session_state.done)}/56** learning days marked completed')
        st.progress(len(st.session_state.done)/56)
        st.caption('Progress stays in your current session. Export a JSON backup from My progress to keep it between visits; no account or database is enabled.')
        st.markdown('[Official DUO KNM practice ↗](https://inburgeren.nl/examen-doen/oefenen.jsp)')


def hero(tag,headline,desc,stats=None):
    spans=''.join(f'<span>{E(x)}</span>' for x in (stats or []))
    st.markdown(f'<div class="hero"><div class="eyebrow">{E(tag)}</div><h1>{E(headline)}</h1><p>{E(desc)}</p><div class="strip">{spans}</div></div>',unsafe_allow_html=True)


def home():
    hero('KNM HORIZON / 8-WEEK A2 PROGRAMME','56 days. A wider horizon.',
         'Your complete visual learning path through all seven KNM themes. Detailed A2 Dutch lessons, English explanations, everyday situations and evidence-based review—day by day.',
         ['56 × 120-minute guided lessons','48 actual textbook sections','7 memory routes','180 original quiz questions'])
    c1,c2,c3,c4=st.columns(4)
    c1.metric('Course days',f'{len(st.session_state.done)} / 56')
    c2.metric('Themes', '7')
    c3.metric('Practice sets', '9')
    c4.metric('Scored tests', str(len(st.session_state.graded)))
    st.markdown('### Your next horizon')
    a,b=st.columns([1.5,1])
    with a:
        card('<div class="eyebrow">TODAY’S LEARNING PATH</div><h3>56 small steps, one confident goal</h3><p>The first seven weeks follow the source book’s chapter order. Days 48–49 bring all seven themes together, and Days 50–56 focus on rights, responsibilities and mixed mock exams.</p><p class="captionline">Each day has a 120-minute structure, reading, detailed English notes, a practical choice, visual recall and practice.</p>')
        if st.button('Explore the 56-day roadmap →',type='primary',use_container_width=True):go(PAGES[1])
    with b:
        card('<div class="eyebrow">TODAY’S PRACTICE</div><h3>Speak. Visualise. Retrieve.</h3><p>Don’t only reread the explanation. Build a mental image, say the Dutch sentence, cover the answer, then recall it.</p>')
        if st.button('Enter the Memory Room →',use_container_width=True):go(PAGES[3])
    st.markdown('### Remember seven themes as seven pictures')
    st.caption('Each picture acts as a doorway into a Dutch-life topic: imagine an everyday scene, name the objects in Dutch, and recall the relevant decision.')
    picture_cols=st.columns(7)
    art_files=['nederland.webp','wonen.webp','gezondheid.webp','onderwijs.webp','werk.webp','instanties.webp','bestuur.webp']
    for idx,t in enumerate(DATA['themes']):
        with picture_cols[idx]:
            st.image(str(BASE/'assets'/art_files[idx]),use_container_width=True)
            st.caption(f'{t["icon"]} {t["name"]}')
    st.markdown('### Seven worlds of everyday life')
    cols=st.columns(3)
    for i,t in enumerate(DATA['themes']):
        with cols[i%3]:
            card(f'<div style="font-size:30px">{E(t["icon"])}</div><h3>{E(t["name"])}</h3><p class="captionline">{E(t["intro"])}</p><span class="topic-pill">{len(t["section_ids"])} sections</span>')
            if st.button('Open theme',key='hometh'+str(t['id']),use_container_width=True):
                first=next(d['day'] for d in DATA['days'] if d.get('section')==t['section_ids'][0]);go(PAGES[2],first)
    with st.expander('Source provenance and the current KNM exam'):
        st.write('The textbook contains seven themes and 48 named sections. This app has original explanations and self-authored mock questions. Its Week 8 themes are supplementary, not literal chapters of the uploaded book.')
        st.info(DATA['info']['exam_note'])
        st.link_button('Check DUO’s current exam information',DATA['info']['duo_exam'])


def roadmap():
    hero('THE ENTIRE JOURNEY','Your 56-day course roadmap','Eight weeks of structured, 120-minute A2 Dutch learning. Open any day, keep a reflection, and check a day off only when you have studied it.', ['8 weeks × 7 days','120 minutes per day','Day 56 = last lesson'])
    st.markdown('### One-click daily path')
    st.caption('Week 1 begins with the Netherlands and its history. Later weeks follow housing, health, schools, work, institutions, government and law. Week 8 is supplementary revision. Every day has a 120-minute study structure.')
    roadmap_csv=io.StringIO()
    cw=csv.writer(roadmap_csv)
    cw.writerow(['Day','Week','Type','Textbook section','Lesson','120-minute session','Study confirmation'])
    for row in DATA['days']:
        cw.writerow([row['day'],get_week(row['day']),row['kind'],row.get('section','Supplementary review'),row['title'],120,'Yes' if row['day'] in st.session_state.done else 'Unconfirmed'])
    st.download_button('Download all 56 days as a CSV plan',roadmap_csv.getvalue().encode('utf-8-sig'),'KNM_HORIZON_56_Day_Roadmap.csv',mime='text/csv')
    for w in range(1,9):
        rows=DATA['days'][(w-1)*7:w*7]
        done=sum(d['day'] in st.session_state.done for d in rows)
        t=THEMES.get(w)
        title=t['name'] if t else 'Final KNM preparation'
        with st.expander(f'WEEK {w:02d} — {title} · {done}/7 confirmed days', expanded=(w==get_week(st.session_state.day))):
            st.progress(done/7)
            cols=st.columns(2)
            for idx,day in enumerate(rows):
                with cols[idx%2]:
                    status='✓' if day['day'] in st.session_state.done else '○'
                    desc=f'DAY {day["day"]:02d}  {status}   ·   {day["title"]}'
                    if st.button(desc,key=f'road_{day["day"]}',use_container_width=True):go(PAGES[2],day['day'])
                    if day.get('section'):
                        ch=DATA['chapters'][day['section']]
                        st.caption(ch.get('a2_intro','')[:160]+' · Source section '+str(day['section']))
                    else:
                        st.caption('Cumulative review and exam preparation · Supplementary study module')
            st.caption('The numbered textbook sections are used where available. Final mock days are supplementary study modules, not publisher exercises.')
    st.markdown('---')
    a,b=st.columns(2)
    with a:
        st.info('**Week 7 bridge**: Day 48 revises seven themes, Day 49 focuses on source-supported social customs.')
    with b:
        st.info('**Week 8**: Days 50–56 contain detailed rights/freedom preparation and seven scored 20-question mocks.')


def timetable(day):
    kind=get_day(day)['kind']
    if kind=='final':
        plan=[('Recall & previous corrections',15),('New A2 reading and explanation',25),('Everyday scenarios and dialogue',20),('Cross-theme contrast and vocabulary',25),('20-question scored mock',20),('Answer reflection and notes',15)]
    elif kind in ('review','customs'):
        plan=[('Seven-theme active recall',15),('Detailed Dutch/English reading',25),('Practical situations and comparisons',25),('Visual-memory drill',15),('Vocabulary and speaking',15),('20-question mixed practice',20),('Reflection',5)]
    else:
        plan=[('Recall yesterday’s knowledge',10),('Read A2 Dutch slowly',20),('Detailed English teaching',25),('Everyday situation and dialogue',20),('Visual memory and vocabulary',20),('Chapter checkpoint',10),('Review & written reflection',15)]
    assert sum(v for k,v in plan)==120
    st.markdown('**Your 120-minute learning rhythm**')
    for item,minutes in plan:st.markdown(f'<span class="topic-pill">{E(item)} · {minutes}m</span>',unsafe_allow_html=True)
    st.caption('Pause at any point; the timetable is a guided allocation rather than an automatic countdown.')


def show_steps(steps):
    for i,x in enumerate(steps):
        st.markdown(f'<div class="step-line"><div class="num">{i+1}</div><div>{E(x)}</div></div>',unsafe_allow_html=True)


def vocab(items,namespace,limit=15):
    if not items:return
    items=items[:limit]
    cards=st.columns(3)
    for idx,it in enumerate(items):
        with cards[idx%3]:
            st.markdown(f'<div class="vocab-item"><div class="nl">{E(it["dutch"])}</div><div class="en">{E(it["english"])}</div></div>',unsafe_allow_html=True)


def chapter_content(ch,extended=True):
    st.markdown(f'<div class="section-tag">From the source textbook · Theme {ch["theme"]} · Section {E(ch["id"])} · printed p. {ch["printed_page"]}</div>',unsafe_allow_html=True)
    st.markdown(f'## {ch["title"]}')
    with st.expander('📍 Look at the theme picture — connect it to today’s subject', expanded=False):
        art = {1:'nederland.webp',2:'wonen.webp',3:'gezondheid.webp',4:'onderwijs.webp',5:'werk.webp',6:'instanties.webp',7:'bestuur.webp'}
        st.image(str(BASE/'assets'/art[ch['theme']]),width=390,caption=f'Theme {ch["theme"]} · {THEMES[ch["theme"]]["name"]} — visual study association')
        st.caption('Picture prompt: describe what you see in two simple Dutch sentences, then say how it relates to the lesson.')
    st.markdown('#### 1 / Read the Dutch')
    st.markdown(f'<div class="lesson-reading">{E(ch["a2_intro"])}<br><br>{E(ch["a2_extended"])}</div>',unsafe_allow_html=True)
    speak_prompt(ch['a2_intro'])
    st.markdown('#### 2 / English explanation — beyond memorising')
    card(f'<p>{E(ch["overview"])}</p><p>{E(ch["expanded_english"])}</p><p><b>Why this matters in KNM:</b> {E(ch["why"])}</p>')
    deep = DEEP.get(ch['id'])
    if deep:
        st.markdown('#### 3 / Go deeper: concept-by-concept explanation')
        card(f'<p><b>{E(deep[0])}</b></p><p>{E(deep[1])}</p>', 'Explain it, don’t just memorise it')
        st.warning('**Don’t confuse these:** '+deep[2])
        st.markdown('**A2 sentence to memorise:**')
        st.markdown(f'<div class="lesson-reading" style="font-size:17px">{E(deep[3])}</div>',unsafe_allow_html=True)
    st.markdown('#### 4 / Remember it as a picture')
    memory_chain(ch['memory'])
    st.info(ch['recall_guide'])
    st.markdown('#### 5 / What would you do?')
    card(f'<b>{E(ch["scenario_dutch"])}</b><p>{E(ch["scenario_english"])}</p>','Your everyday-life situation')
    with st.expander('More realistic situations — try three variations'):
        for s in ch['scenarios']:
            st.markdown(f'**{s["name"]}**')
            st.write(s['dutch'])
            st.caption(s['question_en'])
    st.markdown('#### 6 / A useful practical procedure')
    show_steps(ch['practical_steps'])
    st.markdown('#### 7 / A source-based recall check')
    question=ch['check_question'];answer=ch['check_answer']
    with st.expander('Reveal after speaking your answer: '+question):
        st.success(answer)
        st.caption('A study checkpoint, not an official KNM exam item.')
    st.markdown(f'<span class="topic-pill">Focus word: {E(ch["focus_word"])} = {E(ch["focus_translation"])}</span>',unsafe_allow_html=True)


def final_content(day):
    content=DATA['final'][str(day)]
    st.markdown(f'<div class="section-tag">Supplementary revision: not a published textbook chapter</div>',unsafe_allow_html=True)
    st.markdown(f'## {content["title"]}')
    st.info('**Goal:** '+content['goal'])
    for sec in content['sections']:
        st.markdown('#### '+sec['title'])
        st.markdown('<div class="lesson-reading">'+E(sec['dutch'])+'</div>',unsafe_allow_html=True)
        card('<b>Detailed English teaching</b><p>'+E(sec['english'])+'</p>')
        if sec['extra']:
            with st.expander('Additional source notes / example'):
                for x in sec['extra']:st.write(x)
    for dlg in content['dialogues']:
        with st.expander('💬 A2 Dutch dialogue: '+dlg['title'],expanded=True):
            for person,line in dlg['lines']:st.markdown(f'**{person}:** {line}')
            st.caption(dlg['english'])
    st.markdown('### Visual memory')
    memory_chain(content['memory'])
    st.markdown('### Vocabulary to practise')
    vocab(content['words'],f'{day}_v')
    st.markdown('### Cross-theme retrieval')
    t=THEMES[(day-50)%7+1]
    st.write('Connect today’s topic to **'+t['name']+'**: '+t['bridge']['why'])
    if st.button('Go to Day '+str(day)+' practice test',key=f'go_test_{day}',type='primary'):
        st.session_state.qday=day;st.session_state.exam_select=day;go(PAGES[4])


def review_content(day):
    block=DATA['special'][str(day)]
    st.markdown(f'## {block["title"]}')
    st.markdown('<div class="lesson-reading">'+E(block['a2_reading'])+'</div>',unsafe_allow_html=True)
    card('<p>'+E(block['english'])+'</p>','English teaching note')
    memory_chain(block['memory'])
    st.markdown('### Seven-theme A2 revision')
    for theme in DATA['themes']:
        with st.expander(f'{theme["icon"]} Theme {theme["id"]} — {theme["name"]}'):
            st.write(theme['bridge']['why'])
            show_steps(theme['bridge']['steps'])
            selection=theme['section_ids'][:3]
            for sec in selection:
                ch=DATA['chapters'][sec]
                st.markdown(f'**{sec} {ch["title"]}:** {ch["a2_intro"]}')
    st.markdown('### Core vocabulary')
    vocab(block['words'],f'{day}_r')
    if st.button(f'Practice 20 questions for Day {day}',key=f'review_test_{day}',type='primary'):
        st.session_state.qday=day;st.session_state.exam_select=day;go(PAGES[4])


def chapter_checkpoint(day,ch):
    with st.form(f'checkpoint_{day}'):
        st.markdown('**Checkpoint — what do you remember?**')
        st.write(ch['check_question'])
        answer=st.text_input('Write a short A2 Dutch answer',key=f'cp_answer_{day}')
        check=st.form_submit_button('Reveal the source-based answer')
    if check:
        st.success('Suggested answer: '+ch['check_answer'])
        st.caption('This is an open-response self-check. It is not automatically scored.')


def lesson():
    day=st.session_state.day;d=get_day(day)
    hero(f'WEEK {get_week(day):02d} / DAY {day:02d} OF 56',d['title'],
         'Your guided 120-minute Dutch reading, English explanation, realistic situations, visual memory and active recall.',
         [f'Week {get_week(day)}',f'{round(day/56*100,1)}% through the roadmap','A2 Dutch + English'])
    cols=st.columns([1,1.3,1])
    if cols[0].button('← Previous day',disabled=day==1,use_container_width=True):go(PAGES[2],day-1)
    if cols[1].button('Open 56-day roadmap',use_container_width=True):go(PAGES[1])
    if cols[2].button('Next day →',disabled=day==56,use_container_width=True):go(PAGES[2],day+1)
    with st.expander('⏱️ Your complete 120-minute schedule',expanded=True):timetable(day)
    st.markdown('---')
    if d['kind'] in ('chapter','combo'):
        chapter=DATA['chapters'][d['section']]
        chapter_content(chapter)
        if d['kind']=='combo':
            st.divider();chapter_content(DATA['chapters'][d['extraSection']])
        st.markdown('### Make an A2 Dutch sentence')
        for starter,english in SENTENCE_STARTERS:
            st.markdown(f'<span class="topic-pill">{E(starter)} · {E(english)}</span>',unsafe_allow_html=True)
        st.caption('Choose one sentence starter and complete it using today’s key words. Speak it, then write it in your notes below.')
        st.markdown('### Chapter checkpoint')
        chapter_checkpoint(day,chapter)
        st.markdown('### Vocabulary from this textbook theme')
        vocab(THEMES[d['theme']]['vocabulary'],f'day{day}')
    elif d['kind'] in ('review','customs'):review_content(day)
    else:final_content(day)
    st.markdown('---')
    st.markdown('### A quick revision plan for tomorrow')
    if d.get('theme'):
        lenses=CONCEPT_LENS[d['theme']]
        for i,(term,task) in enumerate(lenses):
            st.markdown(f'**Priority {i+1} — {term}:** {task}')
    else:
        st.markdown('**1.** Correct the questions you missed. **2.** Explain the rule in simple Dutch. **3.** Answer a changed real-life scenario without notes.')
    st.markdown('### Finish your lesson')
    notes=st.text_area('My Dutch recap / What I need to review',value=st.session_state.review_notes.get(str(day),''),height=140,key=f'notes_widget_{day}',placeholder='Vandaag heb ik geleerd dat ... / I still need to practise ...')
    st.session_state.review_notes[str(day)]=notes
    checked=day in st.session_state.done
    if st.checkbox('I actually completed the study activities for Day '+str(day),value=checked,key=f'done_checkbox_{day}')!=checked:
        s=set(st.session_state.done)
        if checked:s.discard(day)
        else:s.add(day)
        st.session_state.done=sorted(s)
        st.rerun()
    if day<56 and st.button('Continue to the next day →',type='primary',key=f'next_{day}'):
        go(PAGES[2],day+1)
    st.caption('Completion is self-reported. One quiz cannot prove full long-term mastery.')


def memory_room():
    hero('MEMORY LAB','Build a picture. Recall a Dutch sentence.','Learn with seven visual routes, vocabulary flashcards, picture-to-word associations, and a personal recall test.', ['7 themes','Flashcards','Three-stage retrieval'])
    choice=st.selectbox('Choose a visual memory route',options=[t['id'] for t in DATA['themes']],format_func=lambda i:f'{THEMES[i]["icon"]} {THEMES[i]["name"]}')
    theme=THEMES[choice]
    art_files=['nederland.webp','wonen.webp','gezondheid.webp','onderwijs.webp','werk.webp','instanties.webp','bestuur.webp']
    a,b=st.columns([1,1.4],vertical_alignment='center')
    with a:st.image(str(BASE/'assets'/art_files[choice-1]),use_container_width=True)
    with b:
        st.subheader('Look → say → apply')
        st.write(theme['stories'][2])
        st.markdown('**Speak in Dutch:** '+theme['stories'][3])
    chain=theme['memory_line'].split('→')
    nodes=''.join(f'<div class="mem-node"><span class="symbol">{E(["🗺️","🏡","🩺","🎒","🗳️","📘","⚖️"][i%7])}</span><b>{E(item.strip())}</b></div>' for i,item in enumerate(chain))
    st.markdown('<div class="mem-chain">'+nodes+'</div>',unsafe_allow_html=True)
    card('<h3>Why the visual sequence works</h3><p>'+E(theme['bridge']['why'])+'</p><p><b>Recall prompt:</b> look away, say each stage in simple Dutch, then explain what happens in a real situation.</p>')
    st.markdown('### Three ideas that organise this theme')
    tri=st.columns(3)
    for i,(name,idea) in enumerate(CONCEPT_LENS[choice]):
        with tri[i]:card('<p>'+E(idea)+'</p>',f'{i+1}. {name}')
    st.markdown('### Flashcard trainer')
    words=theme['vocabulary'];key=f'flash_{choice}';i=st.session_state.card_idx.get(key,0)%len(words)
    item=words[i]
    st.markdown(f'<div class="softbox" style="text-align:center;padding:32px"><div class="eyebrow">VOCABULARY CARD {i+1}/{len(words)}</div><div style="font-size:32px;font-weight:900;color:#4D60B7">{E(item["dutch"])}</div>'+ (f'<div style="font-size:19px;margin-top:19px;color:#697894">{E(item["english"])}</div>' if st.session_state.flip else '<div class="captionline" style="margin-top:17px">Try to remember the English meaning before flipping.</div>')+'</div>',unsafe_allow_html=True)
    l,c,r=st.columns(3)
    if l.button('← Previous',key='flashprev',use_container_width=True):st.session_state.card_idx[key]=(i-1)%len(words);st.session_state.flip=False;st.rerun()
    if c.button('Reveal / hide',key='flashflip',use_container_width=True):st.session_state.flip=not st.session_state.flip;st.rerun()
    if r.button('Next →',key='flashnext',use_container_width=True):st.session_state.card_idx[key]=(i+1)%len(words);st.session_state.flip=False;st.rerun()
    st.markdown('### Memory challenge — look away before you reveal')
    st.info('Picture the theme without looking at the diagram. Say the three concepts in Dutch, then explain one real-life situation. Repeat tomorrow and again after three days.')
    st.markdown('### Put the memory into a story')
    for sec in theme['section_ids'][:4]:
        ch=DATA['chapters'][sec]
        with st.expander(f'{sec} · {ch["title"]} · picture + story'):
            memory_chain(ch['memory'])
            st.markdown('**Dutch:** '+ch['scenario_dutch'])
            st.caption(ch['scenario_english'])
            st.info(ch['recall_guide'])
    with st.expander('The three-stage recall technique'):
        st.write('**1. Picture** the sequence without reading. **2. Speak** the Dutch keyword and a complete A2 sentence. **3. Apply** the knowledge to a changed everyday situation. Return a day later and repeat.')


def practice_exams():
    hero('EXAM ARENA','Practise, score, learn.','Nine separate 20-question practice sets: two cumulative revisions plus seven final-week mocks. All questions are supplementary, not official DUO questions.', ['180 multiple-choice questions','3 options each','English corrections'])
    available=[48,49,50,51,52,53,54,55,56]
    day=st.selectbox('Choose exam',available,index=available.index(st.session_state.qday),format_func=lambda d:f'Day {d} · '+get_day(d)['title'],key='exam_select')
    st.session_state.qday=day
    questions=DATA['quiz'][str(day)]
    a=st.session_state.answers.setdefault(str(day),{})
    pos=st.session_state.qposition.get(str(day),0)
    if str(day) in st.session_state.graded:
        score=st.session_state.graded[str(day)]
        st.markdown(f'<div class="results-big"><div>DAY {day} · PRACTICE RESULT</div><b>{score} / 20</b><div>{int(100*score/20)}% correct · Suggested personal goal 16/20, not an official DUO pass mark</div></div>',unsafe_allow_html=True)
        if score>=16:st.success('Personal practice target reached. Revise any individual mistakes.')
        else:st.warning('More revision recommended. Read the explanations and try different scenarios.')
        categories={}
        for i,q in enumerate(questions):
            cat=q['theme'];row=categories.setdefault(cat,[0,0]);row[1]+=1;row[0]+=int(a.get(str(i))==q['correct'])
        st.markdown('#### Per-topic score')
        for cat,(correct,total) in categories.items():st.write(f'**{cat}:** {correct}/{total}')
        st.markdown('#### See every explanation')
        for i,q in enumerate(questions):
            right=a.get(str(i))==q['correct']
            with st.expander(f'{"✅" if right else "❌"} Question {i+1} — {q["question"]}',expanded=not right):
                if not right:st.write('**Correct answer:** '+q['options'][q['correct']])
                st.write('**English:** '+q['explanation_en'])
        if st.button('Retake this exam',key='retake'+str(day)):
            st.session_state.graded.pop(str(day),None);st.session_state.answers[str(day)]={};st.session_state.qposition[str(day)]=0
            for i in range(20):st.session_state.pop(f'exam_response_{day}_{i}',None)
            st.rerun()
        if st.button('Open score tracker',key='exscore'):go(PAGES[5])
        return
    st.caption(f'{len(a)} of 20 answered · Question {pos+1}/20')
    st.progress(len(a)/20)
    q=questions[pos]
    st.markdown('<div class="section-tag">A2 DUTCH QUESTION · '+E(q['theme'])+'</div>',unsafe_allow_html=True)
    st.markdown('### '+q['question'])
    response_key=f'exam_response_{day}_{pos}'
    v=st.radio('Kies het beste antwoord',list(range(3)),index=a.get(str(pos)),format_func=lambda z:f'{"ABC"[z]}. {q["options"][z]}',key=response_key)
    if v is not None:
        a[str(pos)]=v
    left,mid,right=st.columns(3)
    if left.button('← Previous',disabled=pos==0, key='qp',use_container_width=True):st.session_state.qposition[str(day)]=pos-1;st.rerun()
    if mid.button('Question 1',disabled=pos==0,key='qfirst',use_container_width=True):st.session_state.qposition[str(day)]=0;st.rerun()
    if right.button('Next →',disabled=pos==19,key='qn',use_container_width=True):st.session_state.qposition[str(day)]=pos+1;st.rerun()
    st.markdown('#### Go to a question')
    cols=st.columns(5)
    for i in range(20):
        with cols[i%5]:
            if st.button(('●' if str(i) in a else '○')+str(i+1),key=f'qjump_{i}',use_container_width=True):st.session_state.qposition[str(day)]=i;st.rerun()
    if st.button('Check all 20 answers',type='primary',disabled=len(a)!=20,use_container_width=True,key='submit_exam'):
        st.session_state.graded[str(day)]=sum(a.get(str(i))==q['correct'] for i,q in enumerate(questions))
        st.rerun()
    if len(a)<20:st.caption('You can only score a completed 20-question exam. Unfinished exams are not counted as zero.')


def export_payload():
    return {'format':'knm-horizon-progress-1','exported_utc':datetime.now(timezone.utc).isoformat(),
    'done':st.session_state.done,'answers':st.session_state.answers,'graded':st.session_state.graded,
    'review_notes':st.session_state.review_notes,'confidence':st.session_state.confidence}


def my_progress():
    hero('YOUR PROGRESS','Track effort and evidence separately.','A lesson being taught, a lesson you studied, and an exam score are three different things. This page never invents results from earlier conversations.', ['No fabricated scores','Export / import progress','Only self-reported completion'])
    done=st.session_state.done;graded=st.session_state.graded
    c1,c2,c3=st.columns(3)
    c1.metric('Lessons self-confirmed',f'{len(done)} / 56')
    c2.metric('Scored practice exams',f'{len(graded)} / 9')
    c3.metric('Earlier conversation scores','Unknown')
    st.progress(len(done)/56)
    st.markdown('#### Week-by-week coverage')
    for week in range(1,9):
        amt=sum(((week-1)*7+i) in done for i in range(1,8))
        st.markdown(f'Week {week}: **{amt}/7 confirmed days**')
        st.progress(amt/7)
    st.markdown('#### Your actual graded scores')
    if not graded:st.info('No quiz has been submitted in this website session. Earlier unreported scores remain unknown.')
    for d in sorted(graded,key=int):
        st.write(f'**Day {d}:** {graded[d]}/20 ({int(5*graded[d])}% correct)')
    st.markdown('#### A prioritised revision queue from your actual mistakes')
    missed=Counter()
    for exam_day in graded:
        bank=DATA['quiz'].get(str(exam_day))
        recorded=st.session_state.answers.get(str(exam_day),{})
        if bank and len(recorded)==20:
            for i,q in enumerate(bank):
                if recorded.get(str(i))!=q['correct']:
                    missed[q['theme']]+=1
    if missed:
        for i,(topic,n) in enumerate(missed.most_common(6),1):
            st.markdown(f'**Priority {i}. {topic}:** {n} incorrect answer(s). Revisit the relevant chapters, say the correct rule in A2 Dutch, and answer a new situation.')
        st.caption('Queue uses only finished, scored quizzes with complete saved answers. It does not incorporate unknown earlier scores.')
    else:
        st.info('When you submit a mock and miss a question, its topic will appear here. No earlier performance is assumed.')
    st.markdown('#### Confidence self-assessment')
    for theme in DATA['themes']:
        label=theme['name'];cur=st.session_state.confidence.get(str(theme['id']),'Not assessed')
        val=st.selectbox(label,['Not assessed','Needs more practice','Confident (self-assessed)'],index=['Not assessed','Needs more practice','Confident (self-assessed)'].index(cur),key=f'conf_{theme["id"]}')
        st.session_state.confidence[str(theme['id'])]=val
    st.caption('Confidence is self-reported. Even an 80% result on one practice set is not externally verified long-term mastery.')
    st.markdown('#### Save or restore your personal study record')
    record=json.dumps(export_payload(),ensure_ascii=False,indent=2)
    st.download_button('⬇️ Download my progress JSON',data=record,file_name='KNM_HORIZON_my_progress.json',mime='application/json',use_container_width=True)
    uploaded=st.file_uploader('Restore an earlier progress backup',type=['json'])
    if uploaded is not None and st.button('Import this study record',type='primary'):
        try:
            result=json.loads(uploaded.read())
            if result.get('format')!='knm-horizon-progress-1':raise ValueError('Unrecognised progress format')
            new_done=result.get('done',[])
            if not isinstance(new_done,list) or any(type(v) is not int or v<1 or v>56 for v in new_done):raise ValueError('Invalid days')
            st.session_state.done=sorted(set(new_done))
            st.session_state.graded={str(k):int(v) for k,v in result.get('graded',{}).items() if str(k) in DATA['quiz'] and type(v) is int and 0<=v<=20}
            st.session_state.answers={str(k):{str(i):int(v) for i,v in value.items() if str(i).isdigit() and 0<=int(i)<20 and type(v) is int and 0<=v<3} for k,value in result.get('answers',{}).items() if str(k) in DATA['quiz'] and isinstance(value,dict)}
            st.session_state.review_notes={str(k):str(v)[:10000] for k,v in result.get('review_notes',{}).items() if str(k).isdigit()}
            st.session_state.confidence={str(k):str(v) for k,v in result.get('confidence',{}).items() if str(v) in ['Not assessed','Needs more practice','Confident (self-assessed)']}
            st.success('Record restored.');st.rerun()
        except Exception as exc:st.error('Could not load record: '+str(exc))
    st.warning('Streamlit Community Cloud does not provide per-user permanent storage with this project. Save the JSON backup to preserve your results between sessions.')


def guide():
    hero('SOURCE & DEPLOYMENT GUIDE','From book chapters to real-life decisions.','Transparent attribution, study instructions, DUO links, and an explanation of what the app can—and cannot—verify.', ['48 real section headings','Original teaching explanations','Current DUO references'])
    st.markdown('### What comes from the uploaded book?')
    st.write('The seven-theme organisation, all 48 numbered section names, printed-page references and high-level chapter facts are grounded in the uploaded **TaalCompleet KNM** textbook. The longer concept-by-concept explanations, dialogues, mnemonics and quizzes are original supplements and not quotations or official DUO materials. The book does **not** have an independent chapter titled Final KNM preparation.')
    for t in DATA['themes']:
        with st.expander(f'{t["icon"]} {t["name"]} · {len(t["section_ids"])} textbook sections'):
            for sec in t['section_ids']:
                c=DATA['chapters'][sec]
                st.write(f'{sec} — {c["title"]} · printed page {c["printed_page"]}')
    st.markdown('### Important DUO update')
    st.info(DATA['info']['exam_note'])
    st.markdown('**Confirmed by DUO:** The KNM exam is on a computer and lasts **45 minutes**. Content changed on **1 July 2025**. This app’s 20-question practice sets and 80% personal target do **not** replicate official exam length, scoring or thresholds.')
    c1,c2=st.columns(2)
    with c1:st.link_button('Open current DUO exam guidance ↗',DATA['info']['duo_exam'],use_container_width=True)
    with c2:st.link_button('Open official DUO practice ↗',DATA['info']['duo_practice'],use_container_width=True)
    st.markdown('### How the 56-day schedule works')
    st.write('Days 1–47 follow the source book’s chapter sequence, with two short sections paired on Day 42. Day 48 revises all seven themes; Day 49 practises Dutch social customs discussed throughout the book. Days 50–52 deepen rights and responsibilities and Days 53–56 contain cumulative practice mocks. Those later labels are supplementary modules, not titled sections in the PDF.')
    st.markdown('### What does “mastery” mean here?')
    st.write('You may self-confirm a completed lesson, record your confidence and take scored practice exams. The app does not automatically know results from prior conversations. It does not claim externally verified mastery. To strengthen evidence, retry unfamiliar questions and take DUO’s updated official practice tests.')
    st.markdown('### Can it keep my scores?')
    st.write('This lightweight app uses session state, so your answers may be lost after a reload or server restart. Download a JSON study backup on the progress screen and upload it to resume later. No database and no account are included in this release.')
    st.markdown('### Run and deploy')
    st.code('pip install -r requirements.txt\nstreamlit run streamlit_app.py',language='bash')
    st.write('For Streamlit Community Cloud, put the project files in a GitHub repository. Sign into **share.streamlit.io**, choose **Create app → Yup, I have an app**, select your repository and set the main file to `streamlit_app.py`. The deployment must be authorised in your own Streamlit/GitHub account.')

sidebar()
page=st.session_state.page
if page==PAGES[0]:home()
elif page==PAGES[1]:roadmap()
elif page==PAGES[2]:lesson()
elif page==PAGES[3]:memory_room()
elif page==PAGES[4]:practice_exams()
elif page==PAGES[5]:my_progress()
else:guide()
st.markdown('<div class="book-foot">🌅 KNM HORIZON · An original A2 learning studio grounded in the user-provided TaalCompleet KNM course chapters. Not affiliated with DUO or the textbook publisher.</div>',unsafe_allow_html=True)
