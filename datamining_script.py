from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import base64  
import os  

# Configuration variables
LOGIN_URL = "https://www.PM.com/"
LOGIN_EMAIL = ""
LOGIN_PASSWORD = ""

def get_categories(driver):
    driver.switch_to.window(driver.window_handles[-1])
    
    diagram_icon = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "svg.bi-diagram-3-fill"))
    )
    diagram_icon.click()
    
    # Define all categories and their subcategories
    target_categories = {
        'Administration and health infomatics': [],
        'Dermatology': [],
        'Ear, nose and throat': [],
        'Evidence based clinical practice': [],
        'Medicine': [
            'Cardiology',
            'Endocrinology',
            'Gastroenterology',
            'Geriatric medicine',
            'Haematology',
            'Immunology',
            'Infectious diseases',
            'Metabolic medicine',
            'Nephrology',
            'Neurology',
            'Oncology',
            'Palliative care',
            'Pharmacology',
            'Respiratory'
        ],
        'Ophthalmology': [],
        'Paediatrics': [],
        'Psychiatry': [],
        'Surgical and musculoskeletal problems': ['Orthopaedics', 'Rheumatology', 'Surgery'],
        'Women\'s health': ['Contraception', 'Gynaecology', 'Obstetrics']
    }
    
    for main_category, subcategories in target_categories.items():
        try:
            print(f"\nStarting main category: {main_category}")
            
            main_folder = main_category.replace(' ', '_').replace(':', '_').replace('\'', '')
            if not os.path.exists(main_folder):
                os.makedirs(main_folder)
            
            categories = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a.category-on-left[data-catid]"))
            )
            
            for category in categories:
                if category.text.strip() == main_category:
                    print(f"Clicking main category: {main_category}")
                    driver.execute_script("arguments[0].click();", category)
                    time.sleep(2)
                    
                    if not subcategories:
                        print(f"Processing pages for category: {main_category}")
                        pages = WebDriverWait(driver, 10).until(
                            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "ul.list-group a.shownote"))
                        )
                        
                        print(f"Found {len(pages)} pages in {main_category}")
                        
                        for page in pages:
                            try:
                                driver.execute_script("arguments[0].click();", page)
                                time.sleep(2)
                                
                                title = driver.execute_script('return document.querySelector("#PM-title").textContent.trim()')
                                print(f"Processing: {title}")
                                
                                safe_title = title.replace(':', '_').replace('/', '_').replace('\\', '_').replace('*', '_').replace('?', '_').replace('"', '_').replace('<', '_').replace('>', '_').replace('|', '_')
                                
                                pdf_options = {
                                    'printBackground': True,
                                    'paperWidth': 8.27,
                                    'paperHeight': 11.69,
                                    'pageRanges': '2-'
                                }
                                
                                filename = os.path.join(main_folder, f"{safe_title.replace(' ', '_')[:100]}.pdf")
                                result = driver.execute_cdp_cmd('Page.printToPDF', pdf_options)
                                with open(filename, 'wb') as f:
                                    f.write(base64.b64decode(result['data']))
                                print(f"Saved: {filename}")
                                
                            except Exception as e:
                                print(f"Error processing page: {str(e)}")
                                continue
                        
                        print(f"Finished {main_category}, clicking 'All'")
                        all_link = WebDriverWait(driver, 10).until(
                            EC.element_to_be_clickable((By.CSS_SELECTOR, "a.category-on-left[data-catid='ALL'][data-subcatid='0']"))
                        )
                        driver.execute_script("arguments[0].click();", all_link)
                        time.sleep(2)
                        
                    else:
                        for subcategory in subcategories:
                            try:
                                print(f"\nProcessing subcategory: {subcategory}")
                                
                                sub_folder = os.path.join(main_folder, subcategory.replace(' ', '_'))
                                if not os.path.exists(sub_folder):
                                    os.makedirs(sub_folder)
                                
                                subcategory_elements = WebDriverWait(driver, 10).until(
                                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a.list-group-item.category-on-left[data-subcatid]"))
                                )
                                
                                for sub_elem in subcategory_elements:
                                    if subcategory.lower() in sub_elem.text.strip().lower():
                                        print(f"Found subcategory: {sub_elem.text.strip()}")
                                        driver.execute_script("arguments[0].click();", sub_elem)
                                        time.sleep(2)
                                        
                                        pages = WebDriverWait(driver, 10).until(
                                            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "ul.list-group a.shownote"))
                                        )
                                        
                                        print(f"Found {len(pages)} pages in {subcategory}")
                                        
                                        for page in pages:
                                            try:
                                                driver.execute_script("arguments[0].click();", page)
                                                time.sleep(1)
                                                
                                                title = driver.execute_script('return document.querySelector("#PM-title").textContent.trim()')
                                                print(f"Processing: {title}")
                                                
                                                safe_title = title.replace(':', '_').replace('/', '_').replace('\\', '_').replace('*', '_').replace('?', '_').replace('"', '_').replace('<', '_').replace('>', '_').replace('|', '_')
                                                
                                                pdf_options = {
                                                    'printBackground': True,
                                                    'paperWidth': 8.27,
                                                    'paperHeight': 11.69,
                                                    'pageRanges': '2-'
                                                }
                                                
                                                filename = os.path.join(sub_folder, f"{safe_title.replace(' ', '_')[:100]}.pdf")
                                                result = driver.execute_cdp_cmd('Page.printToPDF', pdf_options)
                                                with open(filename, 'wb') as f:
                                                    f.write(base64.b64decode(result['data']))
                                                print(f"Saved: {filename}")
                                                
                                            except Exception as e:
                                                print(f"Error processing page: {str(e)}")
                                                continue
                                        
                                        print(f"Finished {subcategory}, clicking 'All'")
                                        all_link = WebDriverWait(driver, 10).until(
                                            EC.element_to_be_clickable((By.CSS_SELECTOR, "a.category-on-left[data-catid='ALL'][data-subcatid='0']"))
                                        )
                                        driver.execute_script("arguments[0].click();", all_link)
                                        time.sleep(2)
                                        
                                        categories = WebDriverWait(driver, 10).until(
                                            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a.category-on-left[data-catid]"))
                                        )
                                        for cat in categories:
                                            if cat.text.strip() == main_category:
                                                driver.execute_script("arguments[0].click();", cat)
                                                time.sleep(2)
                                                break
                                        break
                                
                            except Exception as e:
                                print(f"Error processing subcategory {subcategory}: {str(e)}")
                                continue
                    break
            
        except Exception as e:
            print(f"Error processing main category {main_category}: {str(e)}")
            continue
    
    return target_categories

def login_to_PM():
    options = webdriver.ChromeOptions()
    options.add_argument('--start-maximized')
    options.add_argument('--kiosk-printing')
    driver = webdriver.Chrome(options=options)
    
    try:
        driver.get(LOGIN_URL)
        
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        
        try:
            cookie_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.ID, "cookieConsent"))
            )
            cookie_button.click()
        except:
            pass
        
        username = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.NAME, "username"))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", username)
        username.clear()
        username.send_keys(LOGIN_EMAIL)
        
        password = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.NAME, "password"))
        )
        password.clear()
        password.send_keys(LOGIN_PASSWORD)
        
        login_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.NAME, "login_new"))
        )
        login_button.click()
        
        resource_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.NAME, "goto_product"))
        )
        resource_button.click()
        
        textbook_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[@href='textbook/textbook.php']"))
        )
        textbook_link.click()
        
        categories = get_categories(driver)
        return driver, categories
        
    except TimeoutException as e:
        print(f"Timed out waiting for page elements to load: {str(e)}")
        driver.quit()
        return None, None
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        driver.quit()
        return None, None

if __name__ == "__main__":
    driver, categories = login_to_PM()
    print("Categories loaded:", len(categories))
    if isinstance(categories, dict):
        for main_cat, sub_cats in categories.items():
            print(f"\n{main_cat}")
            if sub_cats:
                print("Subcategories:", ", ".join(sub_cats))
