"""
API client for inter-system communication and external APIs
"""
import requests
from config import Config
import random

class APIClient:
    """Client for making API requests to other systems and external services"""
    
    @staticmethod
    def get_all_pets_from_shelter(species='all', breed='', age='', gender='', page=1, search=''):
        """Get pets from Shelter Inventory System"""
        try:
            params = {
                'species': species,
                'breed': breed,
                'age': age,
                'gender': gender,
                'page': page,
                'search': search
            }
            response = requests.get(
                f"{Config.SHELTER_SYSTEM_URL}/api/pets/",
                params=params,
                timeout=5
            )
            if response.status_code == 200:
                return response.json()
            return {'pets': [], 'total': 0, 'pages': 0}
        except Exception as e:
            print(f"Error fetching pets from shelter: {e}")
            return {'pets': [], 'total': 0, 'pages': 0}
    
    @staticmethod
    def get_pet_details_from_shelter(pet_id):
        """Get specific pet details from Shelter System"""
        try:
            response = requests.get(
                f"{Config.SHELTER_SYSTEM_URL}/api/pets/{pet_id}",
                timeout=5
            )
            if response.status_code == 200:
                return response.json()
            return None
        except Exception as e:
            print(f"Error fetching pet details: {e}")
            return None
    
    @staticmethod
    def update_pet_status_in_shelter(pet_id, status):
        """Update pet status in Shelter System"""
        try:
            response = requests.put(
                f"{Config.SHELTER_SYSTEM_URL}/api/update-status/",
                json={'pet_id': pet_id, 'status': status},
                timeout=5
            )
            return response.status_code == 200
        except Exception as e:
            print(f"Error updating pet status: {e}")
            return False
    
    @staticmethod
    def get_pet_health_from_vet(pet_id):
        """Get pet health records from Veterinary System"""
        try:
            response = requests.get(
                f"{Config.VETERINARY_SYSTEM_URL}/api/health/{pet_id}",
                timeout=5
            )
            if response.status_code == 200:
                return response.json()
            return None
        except Exception as e:
            print(f"Error fetching health records: {e}")
            return None
    
    @staticmethod
    def schedule_vet_appointment(pet_id, vet_id, date, reason):
        """Schedule appointment in Veterinary System"""
        try:
            response = requests.post(
                f"{Config.VETERINARY_SYSTEM_URL}/api/schedule-appointment/",
                json={
                    'pet_id': pet_id,
                    'vet_id': vet_id,
                    'date': date,
                    'reason': reason
                },
                timeout=5
            )
            return response.json() if response.status_code == 200 else None
        except Exception as e:
            print(f"Error scheduling appointment: {e}")
            return None
    
    @staticmethod
    def get_dog_breeds():
        """Get list of dog breeds from Dog API"""
        try:
            response = requests.get('https://dog.ceo/api/breeds/list/all', timeout=5)
            if response.status_code == 200:
                data = response.json()
                breeds = list(data.get('message', {}).keys())
                return sorted(breeds)
            return []
        except Exception as e:
            print(f"Error fetching dog breeds: {e}")
            return []
    
    @staticmethod
    def get_random_dog_image(breed=''):
        """Get random dog image from Dog API"""
        try:
            if breed:
                url = f'https://dog.ceo/api/breed/{breed.lower()}/images/random'
            else:
                url = 'https://dog.ceo/api/breeds/image/random'
            
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                data = response.json()
                return data.get('message', '')
            return ''
        except Exception as e:
            print(f"Error fetching dog image: {e}")
            return ''
    
    @staticmethod
    def get_cat_breeds():
        """Get list of cat breeds from Cat API"""
        try:
            headers = {}
            if Config.CAT_API_KEY:
                headers['x-api-key'] = Config.CAT_API_KEY
            
            response = requests.get(
                'https://api.thecatapi.com/v1/breeds',
                headers=headers,
                timeout=5
            )
            if response.status_code == 200:
                breeds = response.json()
                return sorted([breed['name'] for breed in breeds])
            return []
        except Exception as e:
            print(f"Error fetching cat breeds: {e}")
            return []
    
    @staticmethod
    def get_cat_breed_info(breed_name):
        """Get detailed cat breed information"""
        try:
            headers = {}
            if Config.CAT_API_KEY:
                headers['x-api-key'] = Config.CAT_API_KEY
            
            response = requests.get(
                'https://api.thecatapi.com/v1/breeds/search',
                params={'q': breed_name},
                headers=headers,
                timeout=5
            )
            if response.status_code == 200:
                breeds = response.json()
                if breeds:
                    return breeds[0]
            return None
        except Exception as e:
            print(f"Error fetching cat breed info: {e}")
            return None


# Export functions for easier importing
get_all_pets_from_shelter = APIClient.get_all_pets_from_shelter
get_pet_details_from_shelter = APIClient.get_pet_details_from_shelter
update_pet_status_in_shelter = APIClient.update_pet_status_in_shelter
get_pet_health_from_vet = APIClient.get_pet_health_from_vet
schedule_vet_appointment = APIClient.schedule_vet_appointment
get_dog_breeds = APIClient.get_dog_breeds
get_random_dog_image = APIClient.get_random_dog_image
get_cat_breeds = APIClient.get_cat_breeds
get_cat_breed_info = APIClient.get_cat_breed_info
