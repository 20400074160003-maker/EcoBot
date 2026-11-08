import streamlit as st
import requests, random, re

st.set_page_config(page_title="EcoBot", page_icon="🌿", layout="wide")

KB = {
"climate change": ("climate, climate crisis", "Climate change means long-term changes in temperatures and weather patterns. Today's rapid warming is mainly caused by human activities that release greenhouse gases, especially burning coal, oil and gas and clearing forests. Effects include heatwaves, changing rainfall, rising sea levels and pressure on ecosystems. Solutions include clean energy, protecting forests, saving energy and preparing communities."),
"global warming": ("global heating, rising temperature", "Global warming is the long-term rise in Earth's average surface temperature. It is mainly caused by extra greenhouse gases from human activities. It is one important part of climate change."),
"greenhouse effect": ("greenhouse gases, carbon dioxide, methane, co2", "The greenhouse effect is a natural process in which gases in the atmosphere absorb and re-radiate heat, keeping Earth warm. Human activities increase gases such as carbon dioxide and methane, strengthening this effect and causing extra warming."),
"air pollution": ("smog, dirty air, vehicle emissions, pm2.5", "Air pollution occurs when harmful gases, smoke or tiny particles enter the air. Sources include vehicles, factories, burning waste and fires. It can harm human health and plants. Cleaner transport, clean energy and avoiding open waste burning can help."),
"water pollution": ("dirty water, river pollution, ocean pollution", "Water pollution happens when harmful substances enter rivers, lakes, groundwater or oceans. Causes include sewage, industrial waste, farm chemicals and plastic litter. It harms aquatic life and can make water unsafe. Wastewater treatment and proper waste disposal help."),
"soil pollution": ("land pollution, contaminated soil", "Soil pollution is the build-up of harmful chemicals or waste in soil. Sources include pesticides, industrial waste, oil and poorly managed rubbish. It can affect crops, soil organisms and groundwater. Safe disposal and careful chemical use help prevent it."),
"plastic pollution": ("microplastics, single use plastic, plastic waste", "Plastic pollution happens when plastic waste builds up in nature. Large pieces can injure wildlife, while tiny pieces called microplastics spread through water and soil. Reduce single-use items, reuse containers and sort recyclable plastics according to local rules."),
"recycling": ("recycle, recyclable materials", "Recycling means collecting and processing used materials to make new products. Paper, metal, glass and some plastics may be recyclable where facilities exist. Follow local sorting rules. Reducing and reusing usually prevent more waste than recycling alone."),
"3rs": ("reduce reuse recycle, three rs", "The 3Rs are Reduce, Reuse and Recycle. Reduce means using fewer resources. Reuse means using an item again or repairing it. Recycle means processing suitable used materials into new products."),
"deforestation": ("forest clearing, cutting trees, forest loss", "Deforestation is the large-scale removal of forests for farming, roads, settlements or mining. It destroys habitats, reduces biodiversity, can increase soil erosion and releases stored carbon. Forest protection and restoration help."),
"biodiversity": ("biological diversity, variety of life, wildlife", "Biodiversity is the variety of living things, including plants, animals, fungi and microorganisms, and the ecosystems they form. It supports pollination, food webs, clean water and healthy soils. Habitat loss, pollution and climate change threaten it."),
"ecosystem": ("habitat, food web, food chain, ecological balance", "An ecosystem is a community of living organisms interacting with each other and with non-living parts of their environment, such as water, air, soil and sunlight. Forests, rivers and ponds are examples."),
"renewable energy": ("clean energy, green energy", "Renewable energy comes from sources that are naturally replenished, such as sunlight, wind, flowing water and geothermal heat. It can reduce emissions compared with fossil fuels, although projects still need careful environmental planning."),
"fossil fuels": ("coal, oil, natural gas, petroleum", "Fossil fuels are coal, oil and natural gas formed from ancient organic matter over millions of years. Burning them releases carbon dioxide and air pollutants. They are non-renewable because they take an extremely long time to form."),
"solar energy": ("solar panels, solar power, sunlight electricity", "Solar energy comes from sunlight. Solar panels convert sunlight into electricity. Solar power produces no direct air pollution while operating, but panels require materials, manufacturing and responsible recycling."),
"wind energy": ("wind turbines, wind power", "Wind energy uses moving air to turn turbine blades and generate electricity. It is renewable and has low emissions during operation. Projects should consider local communities, landscapes and wildlife."),
"hydropower": ("hydroelectricity, hydro electricity, water power, dams", "Hydropower generates electricity using moving or falling water. It is an important renewable electricity source in Bhutan. Dams and changed river flows can affect habitats, fish and communities, so environmental planning is important."),
"ozone layer": ("ozone depletion, ozone hole, ultraviolet", "The ozone layer is a region of the stratosphere that absorbs much of the Sun's harmful ultraviolet radiation. Certain human-made chemicals damaged it. International action under the Montreal Protocol has helped it recover gradually."),
"acid rain": ("acidic rainfall, sulfur dioxide, nitrogen oxides", "Acid rain forms when sulfur dioxide and nitrogen oxides react in the atmosphere and create acidic substances. It can harm lakes, soils, forests and buildings. Cleaner energy and pollution controls help reduce it."),
"composting": ("compost, organic waste, food scraps, biodegradable waste", "Composting is the natural breakdown of suitable organic materials, such as fruit peels and leaves, into a soil-like material. Compost can improve soil and return nutrients. Do not add plastics or chemicals."),
"water conservation": ("save water, water scarcity, drought", "Water conservation means using water carefully and preventing waste. People can repair leaks and turn off taps when not needed. Communities can protect watersheds, reduce pollution and manage supplies responsibly."),
"carbon footprint": ("carbon emissions, greenhouse gas footprint", "A carbon footprint is the total greenhouse-gas emissions linked to a person, product, activity or organisation. It can include transport, electricity, food and waste. Saving energy and choosing lower-emission transport can reduce it."),
"sustainable development": ("sustainability, sustainable living, future generations", "Sustainable development means meeting today's needs while protecting the ability of future generations to meet their needs. It considers the environment, society and the economy together."),
"endangered species": ("threatened animals, extinction, rare species", "An endangered species faces a very high risk of extinction in the wild. Threats include habitat loss, illegal hunting, pollution and climate change. Habitat protection and conservation laws can help."),
"soil erosion": ("topsoil loss, land degradation", "Soil erosion is the removal of topsoil by water, wind or human activities. Deforestation and poor farming can increase it. Vegetation, terracing and careful land management help keep soil in place."),
"glaciers": ("glacier melting, glacial lake, ice melt, glof", "Glaciers are large masses of ice that move slowly over land. Rising temperatures cause many glaciers to lose ice. In mountain regions, glacial lake outburst floods can be a risk, so monitoring and early-warning systems matter."),
"environment in bhutan": ("bhutan environment, bhutan forests, bhutan climate", "Bhutan is known for forests, biodiversity, rivers and mountain ecosystems. Hydropower is an important renewable electricity source. Environmental priorities include protecting forests and wildlife, managing waste, reducing pollution and preparing for climate risks.")
}

FACTS = [
"Forests store carbon and provide habitats for many species.",
"Wetlands can help filter water and reduce flooding.",
"A food web connects many food chains.",
"Solar panels generate electricity from sunlight.",
"Composting returns nutrients from organic waste to soil.",
"Biodiversity helps ecosystems remain healthy and resilient.",
"The ozone layer protects life from much of the Sun's harmful UV radiation.",
"Hydropower uses moving water to generate electricity.",
"Reducing waste usually comes before reusing and recycling.",
"Glaciers are important freshwater stores in many mountain regions."
]

QUIZ = [
("Which gas is a major contributor to human-caused global warming?", ["Oxygen","Carbon dioxide","Helium"], 1),
("Which is a renewable energy source?", ["Coal","Petroleum","Wind"], 2),
("What do the 3Rs stand for?", ["Reduce, Reuse, Recycle","Read, Run, Rest","Repair, Remove, Replace"], 0),
("What is biodiversity?", ["Only forest trees","The variety of life","Only domestic animals"], 1),
("What is compost usually made from?", ["Organic waste","Glass bottles","Metal cans"], 0)
]

def words(s):
    stop = {"what","is","are","the","a","an","of","how","why","does","do","can","tell","me","about","explain","please","in","and","to","for"}
    return set(re.findall(r"[a-z0-9]+", s.lower())) - stop

def local_answer(q):
    ql = q.lower()
    qw = words(q)
    best, score = None, 0
    for topic, (aliases, answer) in KB.items():
        for phrase in [topic] + aliases.split(", "):
            s = 6 + len(phrase.split()) if phrase in ql else len(words(phrase) & qw)
            if s > score:
                best, score = topic, s
    return (best, KB[best][1]) if best and score >= 1 else (None, None)

def online_search(q):
    try:
        r = requests.get("https://en.wikipedia.org/w/api.php",
            params={"action":"query","list":"search","srsearch":q+" environment climate","format":"json","srlimit":3},
            headers={"User-Agent":"EcoBotSchoolProject/1.0"}, timeout=8)
        r.raise_for_status()
        hits = r.json().get("query",{}).get("search",[])
        output = []
        for hit in hits[:3]:
            title = hit["title"]
            p = requests.get("https://en.wikipedia.org/api/rest_v1/page/summary/"+requests.utils.quote(title,safe=""),
                headers={"User-Agent":"EcoBotSchoolProject/1.0"}, timeout=8)
            if p.ok:
                d = p.json()
                if d.get("extract"):
                    output.append((title,d["extract"],d.get("content_urls",{}).get("desktop",{}).get("page","")))
        return output
    except requests.RequestException:
        return None

st.markdown("""
<style>
.stApp {background:linear-gradient(145deg,#effaf1,#e5f3e9,#f8fcf8);}
.block-container{max-width:1050px;padding-top:1.5rem}
.hero{background:linear-gradient(120deg,#103d2b,#19734c);padding:28px;border-radius:22px;color:white;margin-bottom:18px}
.hero h1{color:white;font-size:2.5rem;margin:0}.hero p{color:#e1f5e8;margin:8px 0 0}
div[data-testid="stChatMessage"]{background:#ffffffd9;border:1px solid #d8eadc;border-radius:15px}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="hero"><h1>🌿 EcoBot</h1><p>Your green knowledge companion — ask, explore and take action for our planet.</p></div>',unsafe_allow_html=True)

with st.sidebar:
    st.markdown("## 🌱 EcoBot Menu")
    page = st.radio("Explore",["💬 Chat","🌍 Topic Library","✨ Daily Eco-Fact","🧠 Eco Quiz","ℹ️ About"])
    st.divider()
    st.markdown("**Try asking:**")
    for q in ["What causes climate change?","Why are forests important?","How does hydropower work?","What are microplastics?"]:
        if st.button(q,use_container_width=True):
            st.session_state.quick=q
            st.session_state.page="💬 Chat"
            st.rerun()

if "page" in st.session_state and "quick" in st.session_state:
    page="💬 Chat"
else:
    st.session_state.page=page

if page=="💬 Chat":
    st.subheader("💬 Chat with EcoBot")
    st.caption("Ask in your own words. EcoBot checks its topic guide first, then searches online references if needed.")
    if "messages" not in st.session_state:
        st.session_state.messages=[("assistant","Hello! I'm EcoBot 🌱 Ask me about climate, pollution, forests, wildlife, water, energy or sustainability.")]
    for role,msg in st.session_state.messages:
        with st.chat_message(role,avatar="🌿" if role=="assistant" else "🧑‍🎓"):
            st.markdown(msg)
    prompt=st.chat_input("Type your environmental question...")
    if "quick" in st.session_state:
        prompt=st.session_state.pop("quick")
    if prompt:
        st.session_state.messages.append(("user",prompt))
        with st.chat_message("user",avatar="🧑‍🎓"): st.markdown(prompt)
        with st.chat_message("assistant",avatar="🌿"):
            topic,answer=local_answer(prompt)
            if answer:
                st.markdown(answer)
                response=answer
                st.caption("Source: EcoBot's built-in educational topic guide.")
            else:
                with st.spinner("Searching online reference summaries..."):
                    results=online_search(prompt)
                if results:
                    response="I found these online reference summaries:"
                    st.markdown(response)
                    for title,extract,url in results:
                        st.markdown("**"+title+"**")
                        st.write(extract)
                        if url: st.markdown("[Read reference]("+url+")")
                    response += "\n\n" + "\n\n".join([title+": "+extract+" "+url for title,extract,url in results])
                elif results is None:
                    response="I couldn't connect to the online reference service. Please check the internet and try again, or choose a topic from the Topic Library."
                    st.warning(response)
                else:
                    response="I couldn't find a useful reference. Try rephrasing your question or choose a topic from the Topic Library."
                    st.info(response)
            st.session_state.messages.append(("assistant",response))
    if st.button("🗑️ Clear conversation"):
        st.session_state.messages=[("assistant","Chat cleared! What would you like to learn?")]
        st.rerun()

elif page=="🌍 Topic Library":
    st.subheader("🌍 Environmental Topic Library")
    st.write("Open a topic to read its explanation.")
    cols=st.columns(2)
    for i,(topic,(aliases,answer)) in enumerate(KB.items()):
        with cols[i%2]:
            with st.expander(topic.title()):
                st.write(answer)
                st.caption("Related terms: "+aliases)

elif page=="✨ Daily Eco-Fact":
    st.subheader("✨ Daily Environmental Fact")
    if "fact" not in st.session_state: st.session_state.fact=random.choice(FACTS)
    st.info(st.session_state.fact,icon="🌱")
    if st.button("Show another fact"):
        st.session_state.fact=random.choice(FACTS); st.rerun()

elif page=="🧠 Eco Quiz":
    st.subheader("🧠 Test Your Eco-Knowledge")
    if "qi" not in st.session_state: st.session_state.qi=0; st.session_state.score=0; st.session_state.done=False
    if st.session_state.done:
        st.success(f"Quiz completed! Your score: {st.session_state.score}/{len(QUIZ)}")
        if st.button("Try again"):
            st.session_state.qi=0; st.session_state.score=0; st.session_state.done=False; st.rerun()
    else:
        i=st.session_state.qi
        q,opts,correct=QUIZ[i]
        st.progress(i/len(QUIZ)); st.markdown(f"**Question {i+1} of {len(QUIZ)}**")
        choice=st.radio(q,opts,key=f"q{i}")
        if st.button("Submit answer"):
            if opts.index(choice)==correct: st.session_state.score+=1; st.success("Correct!")
            else: st.info("Good try! Correct answer: "+opts[correct])
            st.session_state.qi+=1
            if st.session_state.qi>=len(QUIZ): st.session_state.done=True
            st.rerun()

else:
    st.subheader("ℹ️ About EcoBot")
    st.write("EcoBot is a Class 10 environmental awareness app prototype. It contains prepared explanations for many environmental topics and can search Wikipedia online for additional reference summaries.")
    st.markdown("""
**How it works**
1. It checks the built-in topic guide.
2. If it cannot find a prepared answer, it searches online encyclopedia summaries.
3. It also includes a topic library, daily facts and a quiz.

**Important limitation:** This version is not a fully generative AI chatbot. Online summaries are reference material and may be incomplete. Verify important facts with trusted scientific organisations or official government sources.
""")
    st.caption("Educational prototype • Check important facts before presenting.")
