from datetime import datetime
from typing import List, Dict

from connection import get_connection

# Wrote a simple script to get conference recommendations based 
# on what the user is intrested in. It takes their intresets and 
# sees if any of their intrests appear in the conference name or 
# description.
def get_personal_conference_recommendations(user_id: int) -> List[Dict]:
    conn = None
    try:
        conn = get_connection()
        cur = conn.cursor(dictionary=True)

        cur.execute(
            "SELECT Interest_1, Interest_2, Interest_3 FROM `user` WHERE ID = %s",
            (user_id,)
        )
        row = cur.fetchone()
        if not row:
            print(f"No user found with ID: {user_id}")
            return []
        
        # Extracts users interests
        interests = [row.get("Interest_1"), row.get("Interest_2"), row.get("Interest_3")]
        interests = [i.strip() for i in interests if i and i.strip()]
        
        if not interests:
            print("User has no interests")
            return []

        # Fetch conferences and match with user interests
        cur.execute(
            "SELECT CID, Title, Descrip FROM Conferences"
        )
        conferences = cur.fetchall()
        
        matched_conferences = []
        for conf in conferences:
            title = conf.get("Title", "").lower()
            description = conf.get("Descrip", "").lower()
            matched_interests = []
            for interest in interests:
                interest_lower = interest.lower()
                if interest_lower in title or interest_lower in description:
                    matched_interests.append(interest)
            
            # If any interests matched, add this conference to our results
            if matched_interests:
                conf['Matched_Interests'] = matched_interests
                matched_conferences.append(conf)
        
        # Print the matching conferences
        if not matched_conferences:
            print("There are no conferences with your interests available right now")
            return []
        
        print(f"\nFound {len(matched_conferences)} matching conferences:")
        for conf in matched_conferences:
            print(f"\nConference ID: {conf.get('CID')}")
            print(f"Title: {conf.get('Title')}")
            print(f"Description: {conf.get('Descrip', '')[:100]}...")
            print(f"Matched Interests: {', '.join(conf.get('Matched_Interests', []))}")
        
        return matched_conferences
    
    # Error block
    except Exception as e:
        print(f"Error fetching user interests: {e}")
        return []
    finally:
        if conn:
            conn.close()


if __name__ == "__main__":
    test_user_id = 1
    recs = get_personal_conference_recommendations(test_user_id)