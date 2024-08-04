# %% [md]
# # Retrieval Augmented Generation with Langchain, OpenAI, and PineCone
# This demo will utilize the ability to enrich the output of OpenAIs
# LLM ChatGPT-3.5-turbo. The output will be enriched with information
# obtained from a textbook, stored as PDF document. The topic of the
# interaction is sports and remedial massage.
# In first run, LLM will be prompted to provide information without
# augmentation. In second run LLM will be augmented with information
# and asked to provide the response.
# Augmentation is performed by extracting the content from the document
# embedding it, and returning most similar information from the 
# textbook.
# Firstly, let us make the necessary imports.
# %%
from rag.embedding import GenericTextLoader, TextSplitter, \
    OpenAIEmbedder, Rag
# %% [md]
# Names of the imported classes are desciprions of their purpose. Text
# loading is performed via `GenericTextLoader`, splitting of text into
# smaller sections is the job of the `TextSplitter`. Embedding is
# performed with OpenAIEmbedder, finally `Rag` is there to finalize the
# query and get the resulst.
# Let us now add the source document for augmentation.
# %%
SOUURCE_DOCUMENT = r'C:\Users\marko\Downloads\Sports And Remedial Massage Therapy ( PDFDrive ).pdf'
DOCUMENT_TYPE = 'pdf'
# %% [md]
# Let us read the PDF.
# %%
text_loader = GenericTextLoader(
    source_document=SOURCE_DOCUMENT,
    document_type=DOCUMENT_TYPE
)
text_loader.read_document()
document = text_loader.get_document()
# %% [md]
# Let us take a look how many pages there are in the document.
# %%
print(len(document))
# %% [md]
# Now it is necessary to split the documents into smaller sections, so
# that these sections can be transformed, into numerical text 
# representations.
# %%
splitter = TextSplitter(document=document)
splitter.split_document()
converted_document = splitter.get_converted_document()
# %% [md]
# Let us check the length of the sectioned text.
# %%
print(len(converted_document))
# %% [md]
# In next step we will transform the raw pieces of text into their
# numerical representation. What will also be done is storing the
# texts and vectors into vector database. This allows much smoother
# augmentation of the data.
# %%
embedding = OpenAIEmbedder(pieces_of_text=converted_document)
embedding.embed()
# %% [md]
# Now let us instantiate the retrieval augmentation class. This class
# is designed in such way that it can get unaugmented and augmented
# answers to different queries. Let us firstly take a look at the 
# unaugmented answer.
# Call to the class will look like so.
# %%
rag = Rag()
rag.invoke_chain()
output = rag.get_output()
# %% [md]
# And here is the output.
print(output)
# %% [md]
# Not bad at all.
# Let us take a look now at augmented output.
# %%
augmented_rag = Rag(augmented=True)
augmented_rag.invoke_chain()
augmented_output = rag.get_output()
# %% [md]
# And printing of the result.
# %%
print(augmented_output)
