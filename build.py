kb=open("kb.txt",encoding="utf-8").read().strip();rw=open("kb_rw.txt",encoding="utf-8").read().strip()
assert "`" not in kb+rw and len(kb.splitlines())==len(rw.splitlines())
open("index.html","w",encoding="utf-8").write(open("template.html",encoding="utf-8").read().replace("/*KB*/",kb).replace("/*KBRW*/",rw))
print(len(kb.splitlines()),"EN +",len(rw.splitlines()),"RW Q&A embedded")
