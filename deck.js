const P=require('pptxgenjs'),fs=require('fs');const p=new P();p.layout='LAYOUT_WIDE';
const rd=f=>fs.readFileSync(f,'utf8').trim().split('\n').map(l=>{const i=l.indexOf('|');return[l.slice(0,i),l.slice(i+1)]});const kbE=rd('kb.txt'),kbR=rd('kb_rw.txt');const _x=fs.readFileSync('kb.txt','utf8').trim().split('\n').map(l=>{const i=l.indexOf('|');return[l.slice(0,i),l.slice(i+1)]});
const N='14213D',B='1D4ED8',T='0D9488',G='F4F6FB',F='Segoe UI';
const title=(s,t)=>s.addText(t,{x:0.6,y:0.4,w:12,h:0.8,fontSize:30,bold:true,color:B,fontFace:F,isTextBox:true,margin:0});
function card(s,x,y,w,h,head,body){s.addShape(p.ShapeType.roundRect,{x,y,w,h,fill:{color:'FFFFFF'},line:{color:'DFE5F2'},rectRadius:0.12,shadow:{type:'outer',blur:6,offset:2,angle:90,color:'000000',opacity:0.12}});
 s.addText(head,{x:x+0.25,y:y+0.2,w:w-0.5,h:0.5,fontSize:18,bold:true,color:N,fontFace:F,isTextBox:true,margin:0});
 s.addText(body,{x:x+0.25,y:y+0.8,w:w-0.5,h:h-1,fontSize:14,color:'3B4664',fontFace:F,valign:'top',isTextBox:true,margin:0})}
let s=p.addSlide();s.background={color:N};
s.addText('Inzobere',{x:0.8,y:2,w:11,h:1.2,fontSize:60,bold:true,color:'FFFFFF',fontFace:F,isTextBox:true,margin:0});
s.addText('An NLP FAQ chatbot: TF-IDF, cosine similarity, voice and Kinyarwanda',{x:0.8,y:3.3,w:11,h:0.6,fontSize:22,color:'9FB6FF',fontFace:F,isTextBox:true,margin:0});
s.addText('NLP Project  |  Retrieval-based chatbot',{x:0.8,y:4.3,w:11,h:0.4,fontSize:16,color:'C7D2EE',fontFace:F,isTextBox:true,margin:0});
const sl=(t,f)=>{const x=p.addSlide();x.background={color:G};title(x,t);f(x);return x};
sl('The Assignment, Step by Step',x=>{
 card(x,0.6,1.5,5.9,2.3,'1. NLP task','Text classification and retrieval: match a user question to the best stored answer.');
 card(x,6.8,1.5,5.9,2.3,'2. Dataset','100 hand-written NLP question-answer pairs (stored privately in kb.txt).');
 card(x,0.6,4.1,5.9,2.3,'3. Build & understand','Clean text, TF-IDF vectors, cosine similarity, confidence threshold.');
 card(x,6.8,4.1,5.9,2.3,'4. Present','Dataset, pipeline, logic walkthrough and live demo in 5 to 7 minutes.')});
sl('How the Pipeline Works',x=>{
 ['User question','Clean & tokenize','TF-IDF vector','Cosine similarity','Best answer'].forEach((t,i)=>{
  x.addShape(p.ShapeType.roundRect,{x:0.6+i*2.5,y:2.3,w:2.2,h:1.3,fill:{color:i==4?T:B},line:{color:'FFFFFF'},rectRadius:0.12});
  x.addText(t,{x:0.6+i*2.5,y:2.3,w:2.2,h:1.3,align:'center',valign:'middle',fontSize:16,bold:true,color:'FFFFFF',fontFace:F,isTextBox:true});});
 x.addText('Lowercase, remove punctuation and stop words, light stemming, unigrams + bigrams. If the best score is below the threshold, the bot suggests related questions instead of guessing.',{x:0.6,y:4.3,w:12,h:1.2,fontSize:18,color:'3B4664',fontFace:F,isTextBox:true,margin:0})});
sl('TF-IDF in Simple Words',x=>{
 card(x,0.6,1.5,3.9,3.6,'TF','Term Frequency: how often a word appears in a text.');
 card(x,4.7,1.5,3.9,3.6,'IDF','Inverse Document Frequency: words found everywhere (like "is") count less.');
 card(x,8.8,1.5,3.9,3.6,'Cosine similarity','Compares two vectors by angle. Score near 1 means very similar meaning.');
 x.addText('TF-IDF score = TF x IDF. Answer = the stored question with the highest cosine score.',{x:0.6,y:5.6,w:12,h:0.6,fontSize:18,bold:true,color:N,fontFace:F,isTextBox:true,margin:0})});
sl('Smart Features',x=>{
 card(x,0.6,1.5,3.9,2.4,'Voice input','Ask with the microphone (Chrome). Listen to answers aloud.');
 card(x,4.7,1.5,3.9,2.4,'Kinyarwanda','Ask in Kinyarwanda via a built-in glossary; translate answers in one click.');
 card(x,8.8,1.5,3.9,2.4,'Hidden knowledge','100 answers are never listed; users only see what they ask for.');
 card(x,0.6,4.2,3.9,2.4,'Confidence','Every answer shows a match score.');
 card(x,4.7,4.2,3.9,2.4,'Suggestions','Related-question chips guide the user.');
 card(x,8.8,4.2,3.9,2.4,'Dark and light','Professional responsive design for phone and desktop.')});
sl('How to Run and Demo',x=>{
 x.addText([{text:'Open index.html in Google Chrome',options:{bullet:true,breakLine:true}},{text:'Or run: python run.py, then open localhost:8000',options:{bullet:true,breakLine:true}},{text:'Try: "What is TF-IDF?", "ni iki tokenization", or press the microphone',options:{bullet:true,breakLine:true}},{text:'Try an unknown question to see the fallback suggestions',options:{bullet:true}}],{x:0.8,y:1.8,w:11.5,h:3.5,fontSize:22,color:N,fontFace:F,paraSpaceAfter:14,isTextBox:true,margin:0})});
sl('Conclusion and Next Steps',x=>{
 card(x,0.6,1.5,5.9,3.4,'What I learned','Text cleaning matters; TF-IDF is simple yet strong; thresholds prevent wrong answers.');
 card(x,6.8,1.5,5.9,3.4,'Future work','Add embeddings (BERT), a Kinyarwanda answer bank, and more questions.')});
for(const [LN,kb] of [['English',kbE],['Kinyarwanda',kbR]])for(let i=0;i<kb.length;i+=10){const x=p.addSlide();x.background={color:'FFFFFF'};
 x.addText(`Appendix, ${LN} (${i+1}-${i+10} of 100)`,{x:0.5,y:0.25,w:12,h:0.5,fontSize:20,bold:true,color:B,fontFace:F,isTextBox:true,margin:0});
 const rows=[[{text:'#',options:{bold:true,color:'FFFFFF',fill:{color:B}}},{text:'Question',options:{bold:true,color:'FFFFFF',fill:{color:B}}},{text:'Answer',options:{bold:true,color:'FFFFFF',fill:{color:B}}}]];
 kb.slice(i,i+10).forEach((r,j)=>rows.push([String(i+j+1),{text:r[0],options:{bold:true}},r[1]]));
 x.addTable(rows,{x:0.5,y:0.9,w:12.3,colW:[0.5,3.6,8.2],fontSize:10.5,fontFace:F,color:N,border:{type:'solid',color:'DFE5F2',pt:0.75},valign:'middle'})}
p.writeFile({fileName:'Inzobere_Presentation.pptx'}).then(()=>console.log('ok'));
