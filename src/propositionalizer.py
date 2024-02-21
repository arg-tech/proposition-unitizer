from flask import json
import logging
from utility import get_next_max_id
logging.basicConfig(datefmt='%H:%M:%S',
                    level=logging.DEBUG)

from src.data import Data, AIF
from src.templates import PropositionalizerOutput

class Propositionalizer():
	def __init__(self) -> None:
		pass
	def propositionalizer(self, file_obj):
		data = Data(file_obj)
		if data.is_valid_json(): 				
			extended_json_aif = data.get_aif()
			json_aif = json_dict = extended_json_aif['AIF']	
			if 'nodes' in json_dict and 'locutions' in json_dict and 'edges' in json_dict:	
				nodes, edges  = AIF.get_xAIF_arrays(json_dict, ['nodes', 'edges'])				
				original_nodes = nodes.copy()			
				i_nodes_lis = []
				for nodes_entry in original_nodes:
					propositions = nodes_entry['text']
					node_id = nodes_entry['nodeID'] 
					if propositions not in i_nodes_lis:
						if nodes_entry['type'] == "L":						
							inode_id = get_next_max_id(nodes, "nodeID")
							nodes.append({'text': propositions, 'type':'I','nodeID': inode_id})
							i_nodes_lis.append(propositions)
							y_id = get_next_max_id(nodes, "nodeID")
							nodes.append({'text': 'Default Illocuting', 'type':'YA','nodeID': y_id})
							if edges:	
								edge_id = get_next_max_id(edges, "edgeID")
							else:
								edge_id = 0
							edges.append({'toID': y_id, 'fromID':node_id,'edgeID': edge_id})
							edge_id = get_next_max_id(edges, "edgeID")
							edges.append({'toID': inode_id, 'fromID':y_id,'edgeID': edge_id})

				return PropositionalizerOutput.format_output(nodes, edges, json_aif, extended_json_aif)
			else:
				return("Incorrect json-aif format")
		else:
			return("Incorrect input format")



	####################
	def propositionalizer_default(self, file_obj):	
		json_aif = self.propositionalizer(file_obj) 	
		return json_aif


