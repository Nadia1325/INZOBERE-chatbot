const pptxgen = require("pptxgenjs");
const faq = require("./data/faq.json");
const B="1B4F9C", TEAL="12857A", LIGHT="EAF1FB", INK="14213D", MUTE="5B6B86", F="Calibri";
const p = new pptxgen(); p.layout = "LAYOUT_16x9"; p.title = "Simple FAQ Chatbot (NLP)";
const title = (s, t) => s.addText(t, {x:0.5,y:0.3,w:9,h:0.7,fontFace:F,fontSize:28,bold:true,color:B,isTextBox:true,margin:0});
const body = (s, t, o) => s.addText(t, Object.assign({fontFace:F,fontSize:16,color:INK,isTextBox:true,margin:0,valign:"top"}, o));

// 1 Title
let s = p.addSlide(); s.background = {color:B};
s.addText("Simple FAQ Chatbot", {x:0.6,y:1.5,w:8.8,h:1,fontFace:F,fontSize:44,bold:true,color:"FFFFFF",isTextBox:true,margin:0});
s.addText("My first NLP project: match a question to the closest answer using TF-IDF", {x:0.6,y:2.6,w:8.8,h:0.6,fontFace:F,fontSize:20,color:"DCE8FA",isTextBox:true,margin:0});
s.addText("Voice input  |  English and Kinyarwanda  |  100 questions and answers", {x:0.6,y:4.3,w:8.8,h:0.4,fontFace:F,fontSize:14,color:"DCE8FA",isTextBox:true,margin:0});
s.addNotes("Introduce the project: a chatbot that answers common NLP questions.");

// 2 Assignment
s = p.addSlide(); title(s, "The assignment, step by step");
[["1. NLP task","Text matching for an FAQ chatbot (similar to text classification)."],
 ["2. Dataset","100 question-answer pairs about NLP, in 10 topics. Saved as CSV."],
 ["3. Build","Clean text, TF-IDF, cosine similarity with scikit-learn."],
 ["4. Present","Show the pipeline, how it thinks, and the test results."]].forEach(([h,t],i)=>{
  const x=0.5+(i%2)*4.6, y=1.3+Math.floor(i/2)*1.9;
  s.addShape(p.ShapeType.roundRect,{x,y,w:4.3,h:1.7,fill:{color:LIGHT},line:{color:LIGHT},rectRadius:0.12});
  body(s,h,{x:x+0.25,y:y+0.2,w:3.8,h:0.4,fontSize:18,bold:true,color:B});
  body(s,t,{x:x+0.25,y:y+0.7,w:3.8,h:0.9,fontSize:14});});

// 3 Pipeline
s = p.addSlide(); title(s, "How the chatbot works");
["Clean the text","TF-IDF numbers","Cosine similarity","Best answer"].forEach((h,i)=>{
  const x=0.5+i*2.3;
  s.addShape(p.ShapeType.roundRect,{x,y:1.4,w:2.0,h:1.2,fill:{color:i==3?TEAL:B},line:{color:i==3?TEAL:B},rectRadius:0.12});
  s.addText(h,{x,y:1.4,w:2.0,h:1.2,fontFace:F,fontSize:16,bold:true,color:"FFFFFF",align:"center",valign:"middle",isTextBox:true});
  if(i<3) s.addText(">",{x:x+2.0,y:1.7,w:0.3,h:0.6,fontFace:F,fontSize:24,bold:true,color:MUTE,align:"center",isTextBox:true,margin:0});});
body(s,[
 {text:"Example: ",options:{bold:true,color:B}},{text:"\"explain how the bot works\"",options:{breakLine:true}},
 {text:"1. Clean: ",options:{bold:true,color:B}},{text:"lowercase, remove stopwords, stem, so it becomes: explain chatbot work",options:{breakLine:true}},
 {text:"2. TF-IDF: ",options:{bold:true,color:B}},{text:"each word gets a number. Rare, special words get bigger numbers.",options:{breakLine:true}},
 {text:"3. Similarity: ",options:{bold:true,color:B}},{text:"compare with all 100 stored questions. Score from 0 to 1.",options:{breakLine:true}},
 {text:"4. Answer: ",options:{bold:true,color:B}},{text:"\"How does this chatbot work?\" wins with score 0.58. Below 0.20 the bot says it is not sure."}
],{x:0.5,y:3.0,w:9,h:2.3,fontSize:15,paraSpaceAfter:6});

// 4 Key ideas
s = p.addSlide(); title(s, "Simple ideas behind it");
[["TF","How often a word appears in one text."],["IDF","How rare a word is in all texts. Rare words matter more."],
 ["TF-IDF","TF times IDF. Important words get high scores, common words get low scores."],
 ["Cosine similarity","Measures how close two texts are. 1 means same, 0 means different."]].forEach(([h,t],i)=>{
  const y=1.25+i*1.0;
  s.addShape(p.ShapeType.roundRect,{x:0.5,y,w:2.4,h:0.8,fill:{color:B},line:{color:B},rectRadius:0.1});
  s.addText(h,{x:0.5,y,w:2.4,h:0.8,fontFace:F,fontSize:18,bold:true,color:"FFFFFF",align:"center",valign:"middle",isTextBox:true});
  body(s,t,{x:3.2,y,w:6.3,h:0.8,valign:"middle",fontSize:16});});

// 5 Features
s = p.addSlide(); title(s, "Smart features");
[["Voice input","Press the mic and speak your question (Chrome)."],["English and Kinyarwanda","English is default. Kinyarwanda words are understood, and answers can be translated."],
 ["Organized questions","The 100 questions stay hidden. Press Questions to browse by topic, search, and sort."],["Careful answers","Synonyms, word pairs, and a confidence limit, so it does not guess."]].forEach(([h,t],i)=>{
  const x=0.5+(i%2)*4.6, y=1.3+Math.floor(i/2)*1.9;
  s.addShape(p.ShapeType.roundRect,{x,y,w:4.3,h:1.7,fill:{color:LIGHT},line:{color:LIGHT},rectRadius:0.12});
  body(s,h,{x:x+0.25,y:y+0.2,w:3.8,h:0.4,fontSize:18,bold:true,color:TEAL});
  body(s,t,{x:x+0.25,y:y+0.7,w:3.8,h:0.9,fontSize:14});});

// 6 Results
s = p.addSlide(); title(s, "Results and limits");
s.addText("9 / 10",{x:0.5,y:1.3,w:3.4,h:1.2,fontFace:F,fontSize:60,bold:true,color:TEAL,isTextBox:true,margin:0});
body(s,"reworded test questions answered correctly (top-1 accuracy).",{x:0.5,y:2.5,w:3.4,h:0.9,fontSize:15});
body(s,[
 {text:"Good: fast, simple, easy to explain.",options:{bullet:true,breakLine:true}},
 {text:"Good: works well when words match the stored question.",options:{bullet:true,breakLine:true}},
 {text:"Limit: TF-IDF matches words, not meaning.",options:{bullet:true,breakLine:true}},
 {text:"Limit: Kinyarwanda uses a small word list, not full translation.",options:{bullet:true}}
],{x:4.4,y:1.3,w:5.1,h:2.6,fontSize:16,paraSpaceAfter:10});

// 7 Conclusion
s = p.addSlide(); title(s, "Conclusion and next steps");
body(s,[
 {text:"A retrieval chatbot can be built with only cleaning, TF-IDF and cosine similarity.",options:{bullet:true,breakLine:true}},
 {text:"Next: add more questions and synonyms.",options:{bullet:true,breakLine:true}},
 {text:"Next: use sentence embeddings (Hugging Face) to understand meaning.",options:{bullet:true,breakLine:true}},
 {text:"Next: add full Kinyarwanda questions and answers.",options:{bullet:true}}
],{x:0.5,y:1.3,w:9,h:3,fontSize:20,paraSpaceAfter:14});

// Appendix: all 100 Q&A, one slide per topic
const cats=[...new Set(faq.map(r=>r.category))];
cats.forEach(c=>{
  const rows=faq.map((r,i)=>({...r,n:i+1})).filter(r=>r.category===c);
  const s=p.addSlide();
  s.addText(`All questions and answers: ${c}`,{x:0.4,y:0.15,w:9.2,h:0.4,fontFace:F,fontSize:18,bold:true,color:B,isTextBox:true,margin:0});
  const cell=(t,o={})=>({text:t,options:Object.assign({fontFace:F,fontSize:8.5,color:INK,valign:"middle"},o)});
  const data=[[cell("#",{bold:true,color:"FFFFFF",fill:{color:B}}),cell("Question",{bold:true,color:"FFFFFF",fill:{color:B}}),cell("Answer",{bold:true,color:"FFFFFF",fill:{color:B}})]]
    .concat(rows.map((r,i)=>{const f=i%2?{fill:{color:"FFFFFF"}}:{fill:{color:LIGHT}};return[cell(String(r.n),f),cell(r.question,Object.assign({bold:true},f)),cell(r.answer,f)]}));
  s.addTable(data,{x:0.4,y:0.65,w:9.2,colW:[0.4,2.9,5.9],rowH:0.42,border:{type:"solid",pt:0.5,color:"DBE3F0"},margin:[0.03,0.06,0.03,0.06]});
});
p.writeFile({fileName:"NLP_FAQ_Chatbot.pptx"}).then(()=>console.log("done"));
