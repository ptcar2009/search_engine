from search_engine.inverted_index import inverted_index
from search_engine.input import get_file_paths
if __name__ == "__main__":
    index = inverted_index(get_file_paths())
    
    print(index.idf(word="oi"))
    print(index.W(query="oi legal bacana meu caro bem bem bem bem bem bem", word="bem"))
