from database.DB_connect import DBConnect


class DAO:
    @staticmethod
    def getGenres():
        """
        Generi distinti, in ordine alfabetico, per il dropdown.
        """
        conn = DBConnect.get_connection()
        results = []
        if conn is None:
            print("Connessione fallita")
            return results

        cursor = conn.cursor(dictionary=True)
        query = """SELECT DISTINCT genre
                   FROM genre
                   ORDER BY genre"""
        cursor.execute(query)
        for row in cursor:
            results.append(row["genre"])

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getNodes(genere, voti):
        """
        Una riga per ogni coppia (regista, film) dei film del genere scelto
        con almeno 'voti' voti. Restituisce dizionari con le chiavi
        id, nome, idFilm, voti.
        """
        conn = DBConnect.get_connection()
        results = []
        if conn is None:
            print("Connessione fallita")
            return results

        cursor = conn.cursor(dictionary=True)
        query = """SELECT n.id AS id, n.name AS nome, m.id AS idFilm, r.total_votes AS voti
                   FROM director_mapping d, names n, movie m, genre g, ratings r
                   WHERE d.name_id = n.id
                     AND d.movie_id = m.id
                     AND g.movie_id = m.id
                     AND r.movie_id = m.id
                     AND g.genre = %s
                     AND r.total_votes >= %s"""
        cursor.execute(query, (genere, voti))
        for row in cursor:
            results.append(row)

        cursor.close()
        conn.close()
        return results


    @staticmethod
    def getRegistiInterpreti(genere, voti):
        """
        Coppie (regista, interprete): l'interprete ha recitato in un film
        del regista (del genere scelto, con almeno 'voti' voti).
        """
        conn = DBConnect.get_connection()
        results = []
        if conn is None:
            print("Connessione fallita")
            return results

        cursor = conn.cursor(dictionary=True)
        query = """SELECT DISTINCT d.name_id AS idR, rm.name_id AS idI
                   FROM director_mapping d, role_mapping rm, genre g, ratings r
                   WHERE d.movie_id = rm.movie_id
                     AND g.movie_id = d.movie_id
                     AND r.movie_id = d.movie_id
                     AND rm.category IN ('actor', 'actress')
                     AND g.genre = %s
                     AND r.total_votes >= %s"""
        cursor.execute(query, (genere, voti))
        for row in cursor:
            results.append((row["idR"], row["idI"]))
        cursor.close()
        conn.close()
        return results