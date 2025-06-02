import tkinter as tk
from tkinter import ttk, scrolledtext
import requests
from bs4 import BeautifulSoup
import phonenumbers
from phonenumbers import carrier, timezone, geocoder
import json
import threading
import re
from datetime import datetime
import time
from urllib.parse import quote_plus, urljoin
import random
import urllib3
from concurrent.futures import ThreadPoolExecutor
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class ModernTheme:
    """Modern color scheme and styling"""
    BG_COLOR = "#f0f2f5"
    ACCENT_COLOR = "#1a73e8"
    TEXT_COLOR = "#202124"
    SECONDARY_COLOR = "#5f6368"
    SUCCESS_COLOR = "#34a853"
    ERROR_COLOR = "#ea4335"
    FRAME_BG = "#ffffff"

class WebScraper:
    """Enhanced web scraping with multiple sources"""
    
    USER_AGENTS = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15',
    ]

    SOCIAL_PLATFORMS = {
        'facebook.com': 'Facebook',
        'twitter.com': 'Twitter',
        'linkedin.com': 'LinkedIn',
        'instagram.com': 'Instagram',
        'telegram.org': 'Telegram',
        'whatsapp.com': 'WhatsApp',
        'viber.com': 'Viber',
        'snapchat.com': 'Snapchat',
        'tiktok.com': 'TikTok'
    }

    @staticmethod
    def get_random_user_agent():
        return random.choice(WebScraper.USER_AGENTS)

    @staticmethod
    def get_headers():
        return {
            'User-Agent': WebScraper.get_random_user_agent(),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }

    @staticmethod
    def search_google(query, num_results=10):
        results = []
        try:
            encoded_query = quote_plus(query)
            url = f"https://www.google.com/search?q={encoded_query}&num={num_results}"
            response = requests.get(url, headers=WebScraper.get_headers(), verify=False, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            for div in soup.find_all('div', class_='g'):
                try:
                    title_elem = div.find('h3')
                    link_elem = div.find('a')
                    snippet_elem = div.find('div', class_='VwiC3b')
                    
                    if title_elem and link_elem:
                        title = title_elem.text
                        link = link_elem['href']
                        snippet = snippet_elem.text if snippet_elem else "No description available"
                        
                        if link.startswith('/url?q='):
                            link = link.split('/url?q=')[1].split('&')[0]
                        
                        results.append({
                            'title': title,
                            'link': link,
                            'snippet': snippet
                        })
                except Exception:
                    continue
                    
            time.sleep(random.uniform(1, 2))
            return results
        except Exception as e:
            return [{'title': 'Error', 'link': '', 'snippet': str(e)}]

    @staticmethod
    def search_social_media(phone_number):
        """Search for phone number presence on social media platforms"""
        results = []
        
        # Format number variations for search
        formatted_numbers = [
            phone_number,
            phone_number.replace('+', ''),
            phone_number.replace('+', '00'),
            phone_number.replace('+', '').replace(' ', '')
        ]
        
        for platform_url, platform_name in WebScraper.SOCIAL_PLATFORMS.items():
            try:
                # Search each number format
                for num in formatted_numbers:
                    query = f'site:{platform_url} "{num}"'
                    platform_results = WebScraper.search_google(query, num_results=3)
                    
                    if platform_results and not platform_results[0].get('title', '').startswith('Error'):
                        results.append({
                            'platform': platform_name,
                            'results': platform_results
                        })
                        break  # Found results for this platform
                
                time.sleep(random.uniform(1, 2))
            except Exception:
                continue
        
        return results

    @staticmethod
    def search_data_breaches(phone_number):
        """Search for phone number in data breach discussions and forums"""
        queries = [
            f'site:haveibeenpwned.com "{phone_number}"',
            f'site:ghostproject.fr "{phone_number}"',
            f'site:leak-lookup.com "{phone_number}"',
            f'intext:"{phone_number}" intitle:"data breach" OR intitle:"database leak"',
            f'site:pastebin.com "{phone_number}"'
        ]
        
        results = []
        for query in queries:
            try:
                breach_results = WebScraper.search_google(query, num_results=3)
                if breach_results and not breach_results[0].get('title', '').startswith('Error'):
                    results.extend(breach_results)
                time.sleep(random.uniform(1, 2))
            except Exception:
                continue
        
        return results

    @staticmethod
    def search_phone_reputation(phone_number):
        """Search for phone number reputation and spam reports"""
        reputation_sites = [
            'whocalled.us',
            'tellows.com',
            'whocalledme.com',
            'shouldianswer.com',
            'truecaller.com'
        ]
        
        results = []
        for site in reputation_sites:
            try:
                query = f'site:{site} "{phone_number}"'
                rep_results = WebScraper.search_google(query, num_results=3)
                if rep_results and not rep_results[0].get('title', '').startswith('Error'):
                    results.extend(rep_results)
                time.sleep(random.uniform(1, 2))
            except Exception:
                continue
        
        return results

    @staticmethod
    def search_business_associations(phone_number):
        """Search for business associations of the phone number"""
        queries = [
            f'"{phone_number}" site:linkedin.com',
            f'"{phone_number}" site:yelp.com',
            f'"{phone_number}" site:yellowpages.com',
            f'"{phone_number}" site:bbb.org',
            f'"{phone_number}" intitle:"contact" OR intitle:"about us"'
        ]
        
        results = []
        for query in queries:
            try:
                business_results = WebScraper.search_google(query, num_results=3)
                if business_results and not business_results[0].get('title', '').startswith('Error'):
                    results.extend(business_results)
                time.sleep(random.uniform(1, 2))
            except Exception:
                continue
        
        return results

class PhoneOSINTTool:
    def __init__(self, root):
        self.root = root
        self.root.title("Phone Number OSINT Tool")
        self.root.geometry("1000x700")
        self.root.configure(bg=ModernTheme.BG_COLOR)
        
        # Configure modern style
        self.setup_styles()
        
        # Create main container with padding
        container = ttk.Frame(root, style="Container.TFrame")
        container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title
        title_frame = ttk.Frame(container, style="Container.TFrame")
        title_frame.pack(fill=tk.X, pady=(0, 20))
        
        title_label = ttk.Label(
            title_frame,
            text="Phone Number Intelligence",
            style="Title.TLabel"
        )
        title_label.pack(side=tk.LEFT)
        
        # Search section
        search_frame = ttk.LabelFrame(
            container,
            text="Search",
            style="Card.TLabelframe"
        )
        search_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Input container
        input_container = ttk.Frame(search_frame, style="Container.TFrame")
        input_container.pack(fill=tk.X, padx=15, pady=15)
        
        # Country selector
        country_frame = ttk.Frame(input_container, style="Container.TFrame")
        country_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(
            country_frame,
            text="Country",
            style="FieldLabel.TLabel"
        ).pack(side=tk.LEFT)
        
        self.country_var = tk.StringVar()
        self.country_combo = ttk.Combobox(
            country_frame,
            textvariable=self.country_var,
            width=40,
            style="Modern.TCombobox"
        )
        self.country_combo['values'] = self.get_country_list()
        self.country_combo.pack(side=tk.LEFT, padx=(10, 0))
        self.country_combo.bind('<<ComboboxSelected>>', self.on_country_select)
        
        # Phone number input
        number_frame = ttk.Frame(input_container, style="Container.TFrame")
        number_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(
            number_frame,
            text="Phone Number",
            style="FieldLabel.TLabel"
        ).pack(side=tk.LEFT)
        
        self.phone_entry = ttk.Entry(
            number_frame,
            width=30,
            style="Modern.TEntry"
        )
        self.phone_entry.pack(side=tk.LEFT, padx=(10, 0))
        
        # Search button
        button_frame = ttk.Frame(input_container, style="Container.TFrame")
        button_frame.pack(fill=tk.X)
        
        self.search_button = ttk.Button(
            button_frame,
            text="Search",
            command=self.start_search,
            style="Action.TButton"
        )
        self.search_button.pack(side=tk.LEFT)
        
        # Progress section
        progress_frame = ttk.Frame(container, style="Container.TFrame")
        progress_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.progress_var = tk.DoubleVar()
        self.progress = ttk.Progressbar(
            progress_frame,
            variable=self.progress_var,
            maximum=100,
            style="Modern.Horizontal.TProgressbar"
        )
        self.progress.pack(fill=tk.X)
        
        # Results section
        results_frame = ttk.LabelFrame(
            container,
            text="Results",
            style="Card.TLabelframe"
        )
        results_frame.pack(fill=tk.BOTH, expand=True)
        
        # Results text area
        self.results_text = scrolledtext.ScrolledText(
            results_frame,
            height=20,
            font=("Segoe UI", 10),
            bg=ModernTheme.FRAME_BG,
            fg=ModernTheme.TEXT_COLOR
        )
        self.results_text.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        status_label = ttk.Label(
            container,
            textvariable=self.status_var,
            style="Status.TLabel"
        )
        status_label.pack(fill=tk.X, pady=(10, 0))
        
        # Set default country
        self.country_combo.set("United States (+1)")

    def setup_styles(self):
        """Configure ttk styles for modern appearance"""
        style = ttk.Style()
        
        # Configure frame styles
        style.configure(
            "Container.TFrame",
            background=ModernTheme.BG_COLOR
        )
        
        # Configure label styles
        style.configure(
            "Title.TLabel",
            background=ModernTheme.BG_COLOR,
            foreground=ModernTheme.TEXT_COLOR,
            font=("Segoe UI", 24, "bold")
        )
        
        style.configure(
            "FieldLabel.TLabel",
            background=ModernTheme.BG_COLOR,
            foreground=ModernTheme.SECONDARY_COLOR,
            font=("Segoe UI", 10)
        )
        
        style.configure(
            "Status.TLabel",
            background=ModernTheme.BG_COLOR,
            foreground=ModernTheme.SECONDARY_COLOR,
            font=("Segoe UI", 9)
        )
        
        # Configure button styles
        style.configure(
            "Action.TButton",
            background=ModernTheme.ACCENT_COLOR,
            foreground="white",
            padding=(20, 10),
            font=("Segoe UI", 10, "bold")
        )
        
        # Configure progress bar style
        style.configure(
            "Modern.Horizontal.TProgressbar",
            troughcolor=ModernTheme.BG_COLOR,
            background=ModernTheme.ACCENT_COLOR,
            thickness=6
        )
        
        # Configure card style
        style.configure(
            "Card.TLabelframe",
            background=ModernTheme.FRAME_BG,
            padding=10
        )
        
        style.configure(
            "Card.TLabelframe.Label",
            background=ModernTheme.FRAME_BG,
            foreground=ModernTheme.SECONDARY_COLOR,
            font=("Segoe UI", 11)
        )

    def get_country_list(self):
        """Get a list of countries with their calling codes"""
        countries = []
        for region_code in phonenumbers.SUPPORTED_REGIONS:
            try:
                country_code = phonenumbers.country_code_for_region(region_code)
                country_name = phonenumbers.region_code_for_country_code(country_code)
                # Get the country name from the region code
                for name, code in phonenumbers.COUNTRY_CODE_TO_REGION_CODE.items():
                    if region_code in code:
                        country_name = region_code
                        break
                countries.append(f"{country_name} (+{country_code})")
            except:
                continue
        return sorted(countries)

    def on_country_select(self, event):
        """Handle country selection"""
        selected = self.country_combo.get()
        # Clear any existing + in the phone entry
        current_number = self.phone_entry.get().lstrip('+')
        self.phone_entry.delete(0, tk.END)
        self.phone_entry.insert(0, current_number)

    def get_full_number(self):
        """Combine country code and phone number"""
        selected_country = self.country_combo.get()
        country_code = selected_country.split('(+')[-1].rstrip(')')
        number = self.phone_entry.get().lstrip('+')
        return f"+{country_code}{number}"

    def update_progress(self, value):
        self.progress_var.set(value)
        self.root.update_idletasks()

    def update_status(self, status):
        self.status_var.set(status)
        self.root.update_idletasks()

    def append_result(self, text):
        self.results_text.insert(tk.END, f"{text}\n")
        self.results_text.see(tk.END)
        self.root.update_idletasks()

    def format_result_section(self, title):
        """Format a section title in the results"""
        self.results_text.insert(tk.END, f"\n{title}\n")
        self.results_text.insert(tk.END, "─" * len(title) + "\n")

    def validate_phone_number(self, phone_number):
        try:
            parsed_number = phonenumbers.parse(phone_number)
            return phonenumbers.is_valid_number(parsed_number)
        except:
            return False

    def get_basic_info(self, phone_number):
        try:
            parsed_number = phonenumbers.parse(phone_number)
            country = geocoder.description_for_number(parsed_number, "en")
            carrier_name = carrier.name_for_number(parsed_number, "en")
            time_zones = timezone.time_zones_for_number(parsed_number)
            is_valid = phonenumbers.is_valid_number(parsed_number)
            number_type = phonenumbers.number_type(parsed_number)
            
            # Convert number type to readable format
            type_dict = {
                0: "FIXED_LINE",
                1: "MOBILE",
                2: "FIXED_LINE_OR_MOBILE",
                3: "TOLL_FREE",
                4: "PREMIUM_RATE",
                5: "SHARED_COST",
                6: "VOIP",
                7: "PERSONAL_NUMBER",
                8: "PAGER",
                9: "UAN",
                10: "UNKNOWN",
                27: "EMERGENCY",
                28: "VOICEMAIL"
            }
            
            return {
                "Country": country if country else "Unknown",
                "Carrier": carrier_name if carrier_name else "Unknown",
                "Timezone": time_zones[0] if time_zones else "Unknown",
                "Valid Number": "Yes" if is_valid else "No",
                "Number Type": type_dict.get(number_type, "Unknown")
            }
        except Exception as e:
            return {"Error": str(e)}

    def search_google(self, phone_number):
        results = WebScraper.search_google(f'"{phone_number}"')
        formatted_results = []
        
        for result in results:
            formatted_results.append(f"Title: {result['title']}")
            formatted_results.append(f"Link: {result['link']}")
            formatted_results.append(f"Description: {result['snippet']}")
            formatted_results.append("─" * 50)
        
        return formatted_results if formatted_results else ["No results found"]

    def search_pastebin(self, phone_number):
        results = WebScraper.search_pastebin(phone_number)
        formatted_results = []
        
        for result in results:
            formatted_results.append(f"Title: {result['title']}")
            formatted_results.append(f"Link: {result['link']}")
            formatted_results.append(f"Description: {result['snippet']}")
            formatted_results.append("─" * 50)
        
        return formatted_results if formatted_results else ["No results found"]

    def start_search(self):
        # Clear previous results
        self.results_text.delete(1.0, tk.END)
        phone_number = self.get_full_number()
        
        # Disable search button during search
        self.search_button.state(['disabled'])
        
        # Start search in a separate thread
        thread = threading.Thread(target=self.perform_search, args=(phone_number,))
        thread.daemon = True
        thread.start()

    def perform_search(self, phone_number):
        try:
            # Validate phone number
            self.update_status("Validating phone number...")
            self.update_progress(5)
            
            if not self.validate_phone_number(phone_number):
                self.append_result("❌ Error: Invalid phone number format. Please enter a valid number for the selected country.")
                self.update_status("Ready")
                self.search_button.state(['!disabled'])
                return

            # Get basic information
            self.update_status("Getting basic information...")
            self.update_progress(10)
            basic_info = self.get_basic_info(phone_number)
            
            self.format_result_section("Basic Information")
            for key, value in basic_info.items():
                self.append_result(f"• {key}: {value}")

            # Search social media presence
            self.update_status("Checking social media presence...")
            self.update_progress(25)
            social_results = WebScraper.search_social_media(phone_number)
            
            self.format_result_section("Social Media Presence")
            if social_results:
                for platform_data in social_results:
                    self.append_result(f"📱 {platform_data['platform']} Mentions:")
                    for result in platform_data['results']:
                        self.append_result(f"  • {result['title']}")
                        self.append_result(f"    {result['link']}")
                    self.append_result("─" * 50)
            else:
                self.append_result("No direct social media presence found")

            # Search for data breaches
            self.update_status("Checking data breaches...")
            self.update_progress(40)
            breach_results = WebScraper.search_data_breaches(phone_number)
            
            self.format_result_section("Potential Data Breaches")
            if breach_results:
                for result in breach_results:
                    self.append_result(f"⚠️ {result['title']}")
                    self.append_result(f"  {result['link']}")
                    self.append_result(f"  {result['snippet']}")
                    self.append_result("─" * 50)
            else:
                self.append_result("No data breach records found")

            # Check phone reputation
            self.update_status("Checking phone reputation...")
            self.update_progress(60)
            reputation_results = WebScraper.search_phone_reputation(phone_number)
            
            self.format_result_section("Phone Number Reputation")
            if reputation_results:
                for result in reputation_results:
                    self.append_result(f"📊 {result['title']}")
                    self.append_result(f"  {result['link']}")
                    self.append_result(f"  {result['snippet']}")
                    self.append_result("─" * 50)
            else:
                self.append_result("No reputation information found")

            # Search business associations
            self.update_status("Checking business associations...")
            self.update_progress(75)
            business_results = WebScraper.search_business_associations(phone_number)
            
            self.format_result_section("Business Associations")
            if business_results:
                for result in business_results:
                    self.append_result(f"💼 {result['title']}")
                    self.append_result(f"  {result['link']}")
                    self.append_result(f"  {result['snippet']}")
                    self.append_result("─" * 50)
            else:
                self.append_result("No business associations found")

            # General web presence
            self.update_status("Searching general web presence...")
            self.update_progress(90)
            google_results = WebScraper.search_google(f'"{phone_number}"')
            
            self.format_result_section("Additional Web Mentions")
            if google_results:
                for result in google_results:
                    self.append_result(f"🔍 {result['title']}")
                    self.append_result(f"  {result['link']}")
                    self.append_result(f"  {result['snippet']}")
                    self.append_result("─" * 50)

            # Complete
            self.update_progress(100)
            self.update_status("Search completed")
            self.format_result_section("Search Summary")
            self.append_result(f"✓ Search completed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

        except Exception as e:
            self.append_result(f"\n❌ Error during search: {str(e)}")
            self.update_status("Error occurred")
        
        finally:
            # Re-enable search button
            self.search_button.state(['!disabled'])

def main():
    root = tk.Tk()
    app = PhoneOSINTTool(root)
    root.mainloop()

if __name__ == "__main__":
    main() 