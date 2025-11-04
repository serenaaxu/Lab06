from database.DB_connect import get_connection
from model.automobile import Automobile
from model.noleggio import Noleggio
import mysql.connector
'''
    MODELLO: 
    - Rappresenta la struttura dati
    - Si occupa di gestire lo stato dell'applicazione
    - Interagisce con il database
'''

class Autonoleggio:
    def __init__(self, nome, responsabile):
        self._nome = nome
        self._responsabile = responsabile

    @property
    def nome(self):
        return self._nome

    @nome.setter
    def nome(self, nome):
        self._nome = nome

    @property
    def responsabile(self):
        return self._responsabile

    @responsabile.setter
    def responsabile(self, responsabile):
        self._responsabile = responsabile

    def get_automobili(self) -> list[Automobile] | None:
        """
            Funzione che legge tutte le automobili nel database
            :return: una lista con tutte le automobili presenti oppure None
        """
        # TODO
        try:
            cnx = get_connection() 
            if cnx is None:
                print("Errore di connessione")
                return None
                
            cursor_dict = cnx.cursor(dictionary=True)
            cursor_dict.execute("SELECT * FROM automobile ORDER BY marca, modello")

            result = []
            for row in cursor_dict:
                auto = Automobile(
                    codice=row["codice"],
                    marca=row["marca"],
                    modello=row["modello"],
                    anno=row["anno"],
                    posti=row["posti"],
                    disponibile=bool(row["disponibile"])
                )
                result.append(auto)

            cursor_dict.close()
            cnx.close()
            return result if result else None
            
        except Exception as e:
            print(f"Errore in get_automobili: {e}")
            return None


    def get_automobili_per_modello(self, modello) -> list[Automobile] | None:
        """
            Funzione che recupera una lista con tutte le automobili presenti nel database di una certa marca e modello
            :param modello: il modello dell'automobile
            :return: una lista con tutte le automobili di marca e modello indicato oppure None
        """
        # TODO
        try:
            cnx = get_connection()
            if cnx is None:
                print("Errore di connessione")
                return None
                
            cursor_dict = cnx.cursor(dictionary=True)

            query = """SELECT * FROM automobile WHERE modello = %s ORDER BY marca, anno DESC"""
            cursor_dict.execute(query, (modello,))
            
            result = []
            for row in cursor_dict:
                auto = Automobile(
                    codice=row["codice"],
                    marca=row["marca"],
                    modello=row["modello"],
                    anno=row["anno"],
                    posti=row["posti"],
                    disponibile=bool(row["disponibile"])
                )
                result.append(auto)

            cursor_dict.close()
            cnx.close()

            return result if result else None
            
        except Exception as e:
            print(f"Errore in get_automobili_per_modello: {e}")
            return None