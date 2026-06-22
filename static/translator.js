// Insure Platform Multi-Language Translation System
// Supports English (en), Hindi (hi), and Urdu (ur) with RTL page flow

const dictionary = {
    // Navbar & User Info
    "Welcome, ": { hi: "आपका स्वागत है, ", ur: "خوش آمدید، " },
    "Welcome Admin, ": { hi: "आपका स्वागत है प्रशासक, ", ur: "خوش آمدید ایڈمن، " },
    "Admin Panel": { hi: "प्रशासक पैनल", ur: "ایڈمن پینل" },
    "Edit Profile": { hi: "प्रोफ़ाइल संपादित करें", ur: "پروفائل ایڈٹ کریں" },
    "Logout": { hi: "लॉगआउट", ur: "لاگ آؤٹ" },
    "User View": { hi: "उपयोगकर्ता दृश्य", ur: "صارف کا منظر" },
    
    // Index Hero Section
    "Predictive Analytics Platform": { hi: "अनुमानित विश्लेषिकी मंच", ur: "پیش گوئی کرنے والا پلیٹ فارم" },
    "The Best Insurance Begins Here": { hi: "सबसे अच्छा बीमा यहाँ से शुरू होता है", ur: "بہترین انشورنس یہاں سے شروع ہوتی ہے" },
    "Calculate your customized insurance costs using our high-precision Random Forest machine learning engine. Get instant breakdowns and lifestyle suggestions.": {
        hi: "हमारे उच्च-सटीक रैंडम फ़ॉरेस्ट मशीन लर्निंग इंजन का उपयोग करके अपनी अनुकूलित बीमा लागतों की गणना करें। तत्काल विवरण और जीवनशैली के सुझाव प्राप्त करें।",
        ur: "ہمارے اعلیٰ درست رینڈم فارسٹ مشین لرننگ انجن کا استعمال کرتے ہوئے اپنے حسب ضرورت انشورنس اخراجات کا حساب لگائیں۔ فوری تفصیلات اور طرز زندگی کی تجاویز حاصل کریں۔"
    },
    "Start Estimator": { hi: "अनुमानक शुरू करें", ur: "اندازہ کار شروع کریں" },
    "Edit Demographics": { hi: "जनसांख्यिकी संपादित करें", ur: "آبادیاتی معلومات تبدیل کریں" },
    
    // Estimator Header & Form Labels
    "Instant Premium Estimator": { hi: "त्वरित प्रीमियम अनुमानक", ur: "فوری پریمیم اندازہ کار" },
    "Your profile values have been pre-filled. Customize inputs below to predict hypothetical scenarios.": {
        hi: "आपके प्रोफ़ाइल मान पहले से भरे हुए हैं। काल्पनिक परिदृश्यों की भविष्यवाणी करने के लिए नीचे दिए गए इनपुट को अनुकूलित करें।",
        ur: "آپ کے پروفائل کی تفصیلات پہلے سے بھری ہوئی ہیں۔ فرضی منظرناموں کی پیش گوئی کرنے کے لیے نیچے دیے گئے ان پٹس کو تبدیل کریں۔"
    },
    "Age": { hi: "उम्र", ur: "عمر" },
    "Sex": { hi: "लिंग", ur: "جنس" },
    "Male": { hi: "पुरुष", ur: "مرد" },
    "Female": { hi: "महिला", ur: "عورت" },
    "Body Mass Index (BMI)": { hi: "बॉडी मास इंडेक्स (BMI)", ur: "باڈی ماس انڈیکس (BMI)" },
    "Dependent Children": { hi: "आश्रित बच्चे", ur: "وابستہ بچے" },
    
    // BMI Helper tool
    "Need to calculate BMI? Toggle here": { hi: "BMI की गणना करने की आवश्यकता है? यहाँ टॉगल करें", ur: "کیا BMI کا حساب لگانا ہے؟ یہاں کلک کریں" },
    "Don't know your BMI? Calculate it here": { hi: "क्या आप अपना BMI नहीं जानते? यहाँ गणना करें", ur: "اپنا BMI नहीं जानते؟ یہاں حساب لگائیں" },
    "Height (cm)": { hi: "ऊंचाई (सेमी)", ur: "قد (سینٹی میٹر)" },
    "Weight (kg)": { hi: "वजन (किग्रा)", ur: "وزن (کلوگرام)" },
    "Calculate & Apply BMI": { hi: "BMI गणना करें और लागू करें", ur: "حساب لگائیں اور BMI لاگو کریں" },
    
    // Smoker and Region Form Labels & Values
    "Smoker Status": { hi: "धूम्रपान की स्थिति", ur: "تمباکو نوشی کی حالت" },
    "Do you smoke?": { hi: "क्या आप धूम्रपान करते हैं?", ur: "کیا آپ سگریٹ پیتے ہیں؟" },
    "Non-Smoker": { hi: "धूम्रपान न करने वाला", ur: "سگریٹ نہ پینے والا" },
    "Smoker": { hi: "धूम्रपान करने वाला", ur: "سگریٹ پینے वाला" },
    "Region": { hi: "क्षेत्र", ur: "علاقہ" },
    "Northeast": { hi: "पूर्वोत्तर", ur: "شمال مشرقی" },
    "Northwest": { hi: "उत्तर-पश्चिम", ur: "شمال مغربی" },
    "Southeast": { hi: "दक्षिण-पूर्व", ur: "جنوب مشرقی" },
    "Southwest": { hi: "दक्षिण-पश्चिम", ur: "جنوب مغربی" },
    "Calculate Premium": { hi: "प्रीमियम की गणना करें", ur: "پریمیم کا حساب لگائیں" },
    
    // Premium Results Card
    "Prediction Engine": { hi: "भविष्यवाणी इंजन", ur: "پیش گوئی کا انجن" },
    "Modify form values and click \"Calculate Premium\" to get your estimated premium quote.": {
        hi: "अनुमानित प्रीमियम कोट प्राप्त करने के लिए फ़ॉर्म मानों को संशोधित करें और \"प्रीमियम की गणना करें\" पर क्लिक करें।",
        ur: "اندازہ شدہ پریمیم کوٹ حاصل کرنے کے لیے فارم کی قیمتوں کو تبدیل کریں اور \"پریمیم کا حساب لگائیں\" پر کلک کریں۔"
    },
    "Retrieving AI Prediction...": { hi: "AI भविष्यवाणी प्राप्त की जा रही है...", ur: "مصنوعی ذہانت کی پیش گوئی حاصل کی جا رہی ہے..." },
    "Predicted Charge": { hi: "अनुमानित शुल्क", ur: "پیش گوئی شدہ رقم" },
    "Age / Sex": { hi: "उम्र / लिंग", ur: "عمر / جنس" },
    "BMI Value": { hi: "BMI मान", ur: "BMI کی قیمت" },
    "Dependents": { hi: "आश्रितों", ur: "عزیز و اقارب" },
    "Lifestyle Adjustments": { hi: "जीवन शैली समायोजन", ur: "طرز زندگی میں تبدیلیاں" },
    "Save Quote to Database": { hi: "डेटाबेस में कोट सहेजें", ur: "ڈیٹا بیس में कोٹ محفوظ کریں" },
    "Saving Quote...": { hi: "कोट सहेजा जा रहा है...", ur: "کوٹ محفوظ ہو رہا ہے..." },
    "Saved Successfully": { hi: "सफलतापूर्वक सहेजा गया", ur: "کامیابی سے محفوظ ہو گیا" },
    
    // DB status
    "Database: Connected": { hi: "डेटाबेस: जुड़ा हुआ है", ur: "ڈیٹا بیس: منسلک ہے" },
    "Database: Connected (MongoDB)": { hi: "डेटाबेस: जुड़ा हुआ है (MongoDB)", ur: "ڈیٹا بیس: منسلک ہے (MongoDB)" },
    "Database: Offline (SQLite Fallback)": { hi: "डेटाबेस: ऑफ़लाइन (SQLite फ़ालबैक)", ur: "ڈیٹا بیس: آف لائن (SQLite متبادل)" },
    "Database: Offline (Unreachable)": { hi: "डेटाबेस: ऑफ़लाइन (पहुंच से बाहर)", ur: "ڈیٹا بیس: آف لائن (ناقابل رسائی)" },
    
    // History Section & Filters
    "Your Saved Calculations": { hi: "आपकी सहेजी गई गणनाएं", ur: "آپ کے محفوظ کردہ حسابات" },
    "All Smoker Statuses": { hi: "सभी धूम्रपान स्थितियां", ur: "تمباکو نوشی کی تمام حالتیں" },
    "Smokers": { hi: "धूम्रपान करने वाले", ur: "تمباکو نوشی کرنے والے" },
    "Non-Smokers": { hi: "धूम्रपान न करने वाले", ur: "تمباکو نوشی نہ کرنے والے" },
    "All Regions": { hi: "सभी क्षेत्र", ur: "تمام علاقے" },
    "Date Calculated": { hi: "गणना की तिथि", ur: "حساب لگانے की तारीख" },
    "Charges Quote": { hi: "शुल्क कोट", ur: "چارجز کوٹ" },
    "Actions": { hi: "कार्रवाई", ur: "اقدامات" },
    "Fetching saved quotes...": { hi: "सहेजे गए कोट प्राप्त किए जा रहे हैं...", ur: "محفوظ کردہ کوٹس حاصل کیے جا رہے ہیں..." },
    "No quotes saved in your history list yet.": { hi: "अभी तक आपकी इतिहास सूची में कोई कोट सहेजा नहीं गया है।", ur: "ابھی تک آپ کی تاریخ میں کوئی کوٹ محفوظ نہیں کیا گیا ہے۔" },
    "Failed to retrieve history logs.": { hi: "इतिहास लॉग प्राप्त करने में विफल।", ur: "حسابات کی تاریخ حاصل کرنے میں ناکامی۔" },
    "YES": { hi: "हाँ", ur: "جی ہاں" },
    "NO": { hi: "नहीं", ur: "جی نہیں" },
    
    // BMI Categories
    "Underweight": { hi: "अल्पवजन", ur: "کم وزن" },
    "Healthy": { hi: "स्वस्थ", ur: "صحت مند" },
    "Overweight": { hi: "अधिक वजन", ur: "زائد وزن" },
    "Obese": { hi: "मोटापा", ur: "موٹاپا" },
    
    // Dynamic text parts (lifestyle adjustments)
    "Quitting smoking could save you up to ": { hi: "धूम्रपान छोड़ने से आप प्रति वर्ष ", ur: "تمباکو نوشی چھوڑنے سے آپ سالانہ " },
    "Reaching a healthy BMI (22.0) could save you up to ": { hi: "एक स्वस्थ BMI (22.0) तक पहुँचने से आप प्रति वर्ष ", ur: "صحت مند BMI (22.0) حاصل کرنے سے آپ سالانہ " },
    " per year!": { hi: " तक बचा सकते हैं!", ur: " تک بچا سکتے ہیں!" },
    
    // Footer Section
    "Providing intelligent premium forecasting services. Powered by secure machine learning models.": {
        hi: "बुद्धिमान प्रीमियम पूर्वानुमान सेवाएं प्रदान करना। सुरक्षित मशीन लर्निंग मॉडल द्वारा संचालित।",
        ur: "ذہین پریمیم پیش گوئی کی خدمات فراہم کرنا۔ محفوظ مشین لرننگ ماڈلز کے تعاون سے۔"
    },
    "Insurance Solutions": { hi: "बीमा समाधान", ur: "انشورنس سلوشنز" },
    "Health Cover": { hi: "स्वास्थ्य कवर", ur: "صحت کا کور" },
    "Family Coverage": { hi: "पारिवारिक कवरेज", ur: "خاندانی کوریج" },
    "Corporate Benefits": { hi: "कॉर्पोरेट लाभ", ur: "کارپوریٹ فوائد" },
    "Life Insurance": { hi: "जीवन बीमा", ur: "زندگی کی انشورنس" },
    "Resources": { hi: "संसाधन", ur: "وسائل" },
    "Interactive Dashboard": { hi: "इंटरएक्टिव डैशबोर्ड", ur: "انٹرایکٹو ڈیش بورڈ" },
    "How AI Predicts Plan Rates": { hi: "AI योजना दरों की भविष्यवाणी कैसे करता है", ur: "مصنوعی ذہانت پلان کی شرحوں کی پیش گوئی کیسے کرتی ہے" },
    "Health FAQ": { hi: "स्वास्थ्य अक्सर पूछे जाने वाले प्रश्न (FAQ)", ur: "صحت کے متعلق سوالات" },
    "Security Terms": { hi: "सुरक्षा शर्तें", ur: "سیکیورٹی کی شرائط" },
    "Contact Us": { hi: "संपर्क करें", ur: "ہم سے رابطہ کریں" },
    "123 Premium Way, City Centre": { hi: "123 प्रीमियम वे, सिटी सेंटर", ur: "123 پریمیم وے، سٹی سینٹر" },
    "Email: support@insure.com": { hi: "ईमेल: support@insure.com", ur: "ای میل: support@insure.com" },
    "Tel: +1 (555) 123-4567": { hi: "दूरभाष: +1 (555) 123-4567", ur: "فون: +1 (555) 123-4567" },
    "Protected by MongoDB Encryption & Fallback Protocols": { hi: "MongoDB एन्क्रिप्शन और फ़ालबैक प्रोटोकॉल द्वारा सुरक्षित", ur: "MongoDB انکرپشن اور فال بیک پروٹوکول کے ذریعے محفوظ" },
    
    // Auth Pages - Login / Signup / Profile Create
    "Welcome Back": { hi: "आपका स्वागत है", ur: "خوش آمدید" },
    "Username or Email": { hi: "उपयोगकर्ता नाम या ईमेल", ur: "صارف کا نام یا ای میل" },
    "Password": { hi: "पासवर्ड", ur: "پاس ورڈ" },
    "Log In": { hi: "लॉग इन करें", ur: "لاگ ان کریں" },
    "Don't have an account?": { hi: "क्या आपके पास खाता नहीं है?", ur: "کیا آپ کا اکاؤنٹ نہیں ہے؟" },
    "Sign Up": { hi: "साइन अप करें", ur: "سائن اپ کریں" },
    "Create Account": { hi: "खाता बनाएं", ur: "اکاؤنٹ بنائیں" },
    "Confirm Password": { hi: "पासवर्ड की पुष्टि करें", ur: "پاس ورڈ کی تصدیق کریں" },
    "Already have an account?": { hi: "क्या आपके पास पहले से ही एक खाता है?", ur: "پہلے سے ہی ایک اکاؤنٹ ہے؟" },
    "Username": { hi: "उपयोगकर्ता नाम", ur: "صارف کا نام" },
    "Email Address": { hi: "ईमेल पता", ur: "ای میل ایڈریس" },
    "Set Up Profile": { hi: "प्रोफ़ाइल सेट करें", ur: "پروفائل مرتب کریں" },
    "Profile Setup": { hi: "प्रोफ़ाइल सेटअप", ur: "پروفائل سیٹ اپ" },
    "Update Profile": { hi: "प्रोफ़ाइल अपडेट करें", ur: "پروفائل اپ ڈیٹ کریں" },
    "Tell us a bit about yourself to initialize premium analytics": { hi: "प्रीमियम विश्लेषिकी शुरू करने के लिए हमें अपने बारे में थोड़ा बताएं", ur: "پریمیم تجزیات شروع کرنے کے لئے ہمیں اپنے بارے میں بتائیں" },
    "First Name": { hi: "पहला नाम", ur: "پہلا نام" },
    "Last Name": { hi: "अंतिम नाम", ur: "آخری नाम" },
    "Save Profile Changes": { hi: "प्रोफ़ाइल परिवर्तन सहेजें", ur: "پروفائل کی تبدیلیاں محفوظ کریں" },
    "Complete Registration": { hi: "पंजीकरण पूरा करें", ur: "رجسٹریشن مکمل کریں" },
    "Choose a username": { hi: "उपयोगकर्ता नाम चुनें", ur: "صارف کا نام منتخب کریں" },
    "you@example.com": { hi: "you@example.com", ur: "you@example.com" },
    "At least 6 characters": { hi: "कम से कम 6 वर्ण", ur: "کم از کم 6 حروف" },
    "Re-enter password": { hi: "पासवर्ड दोबारा दर्ज करें", ur: "دوبारण پاس ورڈ درج کریں" },
    "Enter username or email": { hi: "उपयोगकर्ता नाम या ईमेल दर्ज करें", ur: "صارف نام یا ای میل درج کریں" },
    "e.g. John": { hi: "जैसे: जॉन", ur: "مثال کے طور پر: جان" },
    "e.g. Doe": { hi: "जैसे: डो", ur: "مثال کے طور پر: ڈو" },
    "e.g. 30": { hi: "जैसे: 30", ur: "مثال کے طور पर: 30" },
    "e.g. 24.5": { hi: "जैसे: 24.5", ur: "مثال کے طور पर: 24.5" },
    "e.g. 0": { hi: "जैसे: 0", ur: "مثال کے طور पर: 0" },
    "e.g. 28": { hi: "जैसे: 28", ur: "مثال کے طور पर: 28" },

    // Admin Dashboard Specific
    "Administrative Data Hub": { hi: "प्रशासनिक डेटा हब", ur: "انتظامی ڈیٹا ہب" },
    "Review system users, profiles, forecast calculations, and demographic analytics.": {
        hi: "सिस्टम उपयोगकर्ताओं, प्रोफ़ाइलों, पूर्वानुमान गणनाओं और जनसांख्यिकीय विश्लेषणों की समीक्षा करें।",
        ur: "سسٹم کے صارفین، پروفائلز، پیش گوئیوں اور آبادیاتی تجزیوں کا جائزہ لیں۔"
    },
    "Download PDF Report": { hi: "PDF रिपोर्ट डाउनलोड करें", ur: "پی ڈی ایف رپورٹ ڈاؤن لوڈ کریں" },
    "Print Report": { hi: "रिपोर्ट प्रिंट करें", ur: "رپورٹ پرنٹ کریں" },
    "Export Excel Sheet (CSV)": { hi: "एक्सेल शीट निर्यात करें (CSV)", ur: "ایکسل شیٹ برآمد کریں (CSV)" },
    "Total Accounts": { hi: "कुल खाते", ur: "کل اکاؤنٹس" },
    "Profiles Completed": { hi: "पूर्ण प्रोफ़ाइल", ur: "مکمل شدہ پروفائلز" },
    "Total Saved Quotes": { hi: "कुल सहेजे गए कोट", ur: "کل محفوظ شدہ کوٹس" },
    "Average Premium": { hi: "औसत प्रीमियम", ur: "اوسط پریمیم" },
    "Demographics & Lifestyle Ratio": { hi: "जनसांख्यिकी और जीवन शैली अनुपात", ur: "آبادیاتی اور طرز زندگی کا تناسب" },
    "Average Premium Charges by Region": { hi: "क्षेत्र के अनुसार औसत प्रीमियम शुल्क", ur: "علاقے کے لحاظ سے اوسط پریمیم چارجز" },
    "Population BMI Category Distribution": { hi: "जनसंख्या BMI श्रेणी वितरण", ur: "آبادی کا BMI زمرہ وار پھیلاؤ" },
    "User Directory & Associated Profiles": { hi: "उपयोगकर्ता निर्देशिका और संबद्ध प्रोफ़ाइल", ur: "صارفین کی فہرست اور متعلقہ پروفائلز" },
    "Plain passwords are protected. Showing secure hashes.": { hi: "सादे पासवर्ड सुरक्षित हैं। सुरक्षित हैश दिखा रहा है।", ur: "سادہ پاس ورڈز محفوظ ہیں۔ صرف ہیشز دکھائے جا رہے ہیں۔" },
    "User ID": { hi: "उपयोगकर्ता ID", ur: "صارف کی شناخت" },
    "Password Hash": { hi: "पासवर्ड हैश", ur: "پاس ورڈ ہیش" },
    "Admin?": { hi: "प्रशासक?", ur: "ایڈمن؟" },
    "YES": { hi: "हाँ", ur: "جی ہاں" },
    "NO": { hi: "नहीं", ur: "جی نہیں" },
    "Name": { hi: "नाम", ur: "نام" },
    "Quotes": { hi: "कोट", ur: "کوٹس" },
    "User Distribution": { hi: "उपयोगकर्ता वितरण", ur: "صارفین کی تقسیم" },
    "Average Predicted Charges ($)": { hi: "औसत अनुमानित शुल्क ($)", ur: "اوسط پیش گوئی شدہ رقم ($)" },
    "Number of Users": { hi: "उपयोगकर्ताओं की संख्या", ur: "صارفین کی تعداد" },
    "Males": { hi: "पुरुष", ur: "مرد" },
    "Females": { hi: "महिलाएं", ur: "خواتین" }
};

window.currentLanguage = localStorage.getItem('selectedLanguage') || 'en';

// Translates the page DOM nodes recursively
window.translatePage = function(lang) {
    window.currentLanguage = lang;
    localStorage.setItem('selectedLanguage', lang);

    // Update body class & document direction for Urdu (RTL)
    if (lang === 'ur') {
        document.documentElement.setAttribute('dir', 'rtl');
        document.documentElement.setAttribute('lang', 'ur');
        document.body.classList.add('rtl-mode');
    } else {
        document.documentElement.setAttribute('dir', 'ltr');
        document.documentElement.setAttribute('lang', lang);
        document.body.classList.remove('rtl-mode');
    }

    // Traverse DOM to update text nodes
    translateNode(document.body, lang);

    // Sync select dropdowns on the page
    document.querySelectorAll('#lang-select').forEach(select => {
        select.value = lang;
    });
};

function translateNode(el, lang) {
    // Ignore script, style, canvas tags, and the language selectors themselves
    if (['SCRIPT', 'STYLE', 'CANVAS', 'SVG'].includes(el.tagName)) return;
    if (el.classList && (el.classList.contains('lang-select') || el.classList.contains('lang-selector-container'))) return;

    if (el.nodeType === Node.TEXT_NODE) {
        const text = el.textContent.trim();
        if (text) {
            // 1. Regular full match translation
            if (dictionary[text]) {
                if (!el.parentElement.hasAttribute('data-orig-text')) {
                    el.parentElement.setAttribute('data-orig-text', text);
                }
                const orig = el.parentElement.getAttribute('data-orig-text');
                el.textContent = el.textContent.replace(text, lang === 'en' ? orig : dictionary[orig][lang]);
            }
            // 2. Specific matching for Dynamic "Or $X,XXX.XX / month" patterns
            else if (/^Or \$[\d,.]+( \/ month)?$/.test(text)) {
                if (!el.parentElement.hasAttribute('data-orig-text')) {
                    el.parentElement.setAttribute('data-orig-text', text);
                }
                const orig = el.parentElement.getAttribute('data-orig-text');
                if (lang === 'en') {
                    el.textContent = orig;
                } else {
                    const match = orig.match(/^Or \$([\d,.]+)( \/ month)?$/);
                    if (match) {
                        const amount = match[1];
                        const isMonthly = !!match[2];
                        if (isMonthly) {
                            el.textContent = lang === 'hi' ? `या $${amount} / महीना` : `یا $${amount} / مہینہ`;
                        } else {
                            el.textContent = lang === 'hi' ? `या $${amount}` : `یا $${amount}`;
                        }
                    }
                }
            }
        }
    } else {
        // Handle input placeholders and option texts
        if (el.tagName === 'INPUT' || el.tagName === 'TEXTAREA') {
            if (el.placeholder && dictionary[el.placeholder.trim()]) {
                const rawPlaceholder = el.placeholder.trim();
                if (!el.hasAttribute('data-orig-placeholder')) {
                    el.setAttribute('data-orig-placeholder', rawPlaceholder);
                }
                const orig = el.getAttribute('data-orig-placeholder');
                el.placeholder = lang === 'en' ? orig : dictionary[orig][lang];
            }
        }

        if (el.tagName === 'OPTION') {
            const rawText = el.textContent.trim();
            if (dictionary[rawText]) {
                if (!el.hasAttribute('data-orig-text')) {
                    el.setAttribute('data-orig-text', rawText);
                }
                const orig = el.getAttribute('data-orig-text');
                el.textContent = lang === 'en' ? orig : dictionary[orig][lang];
            }
        }

        // Recursively translate children
        for (let i = 0; i < el.childNodes.length; i++) {
            translateNode(el.childNodes[i], lang);
        }
    }
}

// Global language switcher method
window.changeLanguage = function(lang) {
    window.translatePage(lang);
};

// Auto-run on page load
document.addEventListener('DOMContentLoaded', () => {
    // Small delay to ensure database statuses or user-customized templates are set up first
    setTimeout(() => {
        window.translatePage(window.currentLanguage);
    }, 50);
});

// Helper for dynamic JS text translations
window.getTranslatedText = function(text, lang) {
    if (lang === 'en' || !dictionary[text]) return text;
    return dictionary[text][lang] || text;
};

