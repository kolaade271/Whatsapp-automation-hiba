class Messages:
    """Centralized message templates for the chatbot"""
    
    def get_welcome_message(self) -> str:
        """Trilingual welcome message"""
        return (
            "مرحبا بكم في فضاء WafR\n"
            "Bienvenue dans l'espace de WafR\n"
            "Welcome to WafR Space\n\n"
            "Entrez 1️⃣ pour le Français\n"
            "أدخلوا 2️⃣ للعربية\n"
            "Enter 3️⃣ for English"
        )
    
    def get_service_menu(self, lang: str) -> str:
        """Service selection menu"""
        if lang == "fr":
            return (
                "Veuillez sélectionner le service désiré:\n\n"
                "1️⃣ Envoyer la Recharge IAM\n"
                "2️⃣ Envoyer la Recharge INWI\n"
                "3️⃣ Envoyer la Recharge ORANGE\n"
                "4️⃣ Consulter mon solde WafR\n"
                "5️⃣ Alimenter mon solde WafR\n"
                "6️⃣ Retirer de mon solde WafR\n"
                "7️⃣ Payer une Facture\n"
                "8️⃣ Envoyer le Cash via CODE\n"
                "9️⃣ Retirer le Cash via CODE\n\n"
                "💡 Tapez *Menu* pour recommencer"
            )
        elif lang == "en":
            return (
                "Please select a service:\n\n"
                "1️⃣ Send IAM Recharge\n"
                "2️⃣ Send INWI Recharge\n"
                "3️⃣ Send ORANGE Recharge\n"
                "4️⃣ Check WafR Balance\n"
                "5️⃣ Top-up WafR Balance\n"
                "6️⃣ Withdraw from WafR Balance\n"
                "7️⃣ Pay a Bill\n"
                "8️⃣ Send Cash via CODE\n"
                "9️⃣ Withdraw Cash via CODE\n\n"
                "💡 Type *Menu* to start over"
            )
        else:  # Arabic
            return (
                "المرجو اختيار الخدمة:\n\n"
                "1️⃣ إرسال تعبئة اتصالات المغرب\n\n"
                "2️⃣ إرسال تعبئة إنوي\n\n"
                "3️⃣ إرسال تعبئة أورنج\n\n"
                "4️⃣ الاطلاع على رصيدي في وفر\n\n"
                "5️⃣ تعبئة رصيدي\n\n"
                "6️⃣ سحب من رصيدي\n\n"
                "7️⃣ أداء فاتورة\n\n"
                "8️⃣ إرسال النقود عبر كود\n\n"
                "9️⃣ سحب النقود عبر كود\n\n"
                "💡 اكتب *القائمة* للبدء من جديد"
            )
    
    def get_coming_soon_message(self, lang: str) -> str:
        """Coming soon message for unavailable services"""
        if lang == "fr":
            return "⏳ Ce service va être disponible prochainement"
        elif lang == "en":
            return "⏳ This service will be available soon"
        else:
            return "⏳ هذه الخدمة ستكون متاحة قريبا"
    
    def get_phone_number_prompt(self, lang: str) -> str:
        """Phone number prompt"""
        if lang == "fr":
            return "📱 Veuillez entrer le numéro de téléphone à recharger:"
        elif lang == "en":
            return "📱 Please enter the phone number to recharge:"
        else:
            return "📱 المرجو إدخال رقم الهاتف المراد تعبئته:"
    
    def get_invalid_phone_message(self, lang: str) -> str:
        """Invalid phone number message"""
        if lang == "fr":
            return "❌ Numéro invalide. Veuillez entrer un numéro valide (ex: 06 12 34 56 78)"
        else:
            return "❌ رقم غير صالح. المرجو إدخال رقم صحيح"
    
    def get_amount_menu(self, lang: str) -> str:
        """Amount selection menu"""
        if lang == "fr":
            return (
                "💰 Veuillez sélectionner le montant de la recharge:\n\n"
                "1️⃣ 5 DH\n"
                "2️⃣ 10 DH\n"
                "3️⃣ 20 DH\n"
                "4️⃣ 25 DH\n"
                "5️⃣ 30 DH\n"
                "6️⃣ 50 DH\n"
                "7️⃣ 100 DH\n"
                "8️⃣ 200 DH\n"
                "9️⃣ 300 DH"
            )
        elif lang == "en":
            return (
                "💰 Please select the recharge amount:\n\n"
                "1️⃣ 5 DH\n"
                "2️⃣ 10 DH\n"
                "3️⃣ 20 DH\n"
                "4️⃣ 25 DH\n"
                "5️⃣ 30 DH\n"
                "6️⃣ 50 DH\n"
                "7️⃣ 100 DH\n"
                "8️⃣ 200 DH\n"
                "9️⃣ 300 DH"
            )
        else:
            return (
                "💰 المرجو اختيار مبلغ التعبئة:\n\n"
                "1️⃣ 5 دراهم\n"
                "2️⃣ 10 دراهم\n"
                "3️⃣ 20 درهم\n"
                "4️⃣ 25 درهم\n"
                "5️⃣ 30 درهم\n"
                "6️⃣ 50 درهم\n"
                "7️⃣ 100 درهم\n"
                "8️⃣ 200 درهم\n"
                "9️⃣ 300 درهم"
            )
    
    def get_offer_menu(self, lang: str) -> str:
        """Offer selection menu"""
        if lang == "fr":
            return (
                "🎁 Veuillez sélectionner l'offre:\n\n"
                "1️⃣ *6 (Réseaux Sociaux)\n"
                "2️⃣ *1 (Appels Nationaux)\n"
                "3️⃣ *2 (Appels Internationaux)\n"
                "4️⃣ *3 (Internet)\n"
                "5️⃣ *5 (Pass Internet)\n"
                "6️⃣ *9 (Illimité)\n"
                "7️⃣ *7 (Pass Étudiant)\n"
                "8️⃣ *8 (Pass Entreprise)\n"
                "9️⃣ *4 (Roaming)\n"
                "🔟 *10 (Jeux)\n"
                "1️⃣1️⃣ *11 (Musique)\n"
                "1️⃣2️⃣ *12 (Vidéo)"
            )
        elif lang == "en":
            return (
                "🎁 Please select the offer:\n\n"
                "1️⃣ *6 (Social Media)\n"
                "2️⃣ *1 (National Calls)\n"
                "3️⃣ *2 (International Calls)\n"
                "4️⃣ *3 (Internet)\n"
                "5️⃣ *5 (Internet Pass)\n"
                "6️⃣ *9 (Unlimited)\n"
                "7️⃣ *7 (Student Pass)\n"
                "8️⃣ *8 (Business Pass)\n"
                "9️⃣ *4 (Roaming)\n"
                "🔟 *10 (Games)\n"
                "1️⃣1️⃣ *11 (Music)\n"
                "1️⃣2️⃣ *12 (Video)"
            )
        else:
            return (
                "🎁 المرجو اختيار العرض:\n\n"
                "1️⃣ *6 (شبكات التواصل)\n"
                "2️⃣ *1 (مكالمات وطنية)\n"
                "3️⃣ *2 (مكالمات دولية)\n"
                "4️⃣ *3 (إنترنت)\n"
                "5️⃣ *5 (باس الإنترنت)\n"
                "6️⃣ *9 (لا محدود)\n"
                "7️⃣ *7 (باس طالب)\n"
                "8️⃣ *8 (باس مقاولة)\n"
                "9️⃣ *4 (تجوال)\n"
                "🔟 *10 (ألعاب)\n"
                "1️⃣1️⃣ *11 (موسيقى)\n"
                "1️⃣2️⃣ *12 (فيديو)"
            )
    
    def get_confirmation_message(self, lang: str, operator: str, phone: str, amount: str, offer: str) -> str:
        """Confirmation message"""
        if lang == "fr":
            return (
                f"📝 *Confirmation*\n\n"
                f"Opérateur: {operator}\n"
                f"Téléphone: {phone}\n"
                f"Montant: {amount} DH\n"
                f"Offre: {offer}\n\n"
                "1️⃣ Confirmer\n"
                "2️⃣ Annuler"
            )
        elif lang == "en":
            return (
                f"📝 *Confirmation*\n\n"
                f"Operator: {operator}\n"
                f"Phone: {phone}\n"
                f"Amount: {amount} DH\n"
                f"Offer: {offer}\n\n"
                "1️⃣ Confirm\n"
                "2️⃣ Cancel"
            )
        else:
            return (
                f"📝 *تأكيد*\n\n"
                f"المشغل: {operator}\n"
                f"الهاتف: {phone}\n"
                f"المبلغ: {amount} درهم\n"
                f"العرض: {offer}\n\n"
                "1️⃣ تأكيد\n"
                "2️⃣ إلغاء"
            )
    
    def get_success_message(self, lang: str) -> str:
        """Success message"""
        if lang == "fr":
            return "✅ Votre opération a été effectuée avec succès"
        elif lang == "en":
            return "✅ Your operation was successful"
        else:
            return "✅ لقد تم إجراء العملية بنجاح"
    
    def get_cancelled_message(self, lang: str) -> str:
        """Cancellation message"""
        if lang == "fr":
            return "❌ Opération annulée"
        elif lang == "en":
            return "❌ Operation cancelled"
        else:
            return "❌ تم إلغاء العملية"
    
    def get_restart_message(self, lang: str) -> str:
        """Restart message"""
        if lang == "fr":
            return "🔄 Conversation réinitialisée."
        elif lang == "en":
            return "🔄 Conversation reset."
        else:
            return "🔄 تم إعادة تعيين المحادثة."
    
    def get_help_message(self, lang: str) -> str:
        """Help message"""
        if lang == "fr":
            return (
                "❓ *Aide*\n\n"
                "Voici les commandes disponibles:\n"
                "• *Menu* - Retourner au menu principal\n"
                "• *Annuler* - Annuler l'opération en cours\n"
                "• *Aide* - Afficher ce message"
            )
        elif lang == "en":
            return (
                "❓ *Help*\n\n"
                "Available commands:\n"
                "• *Menu* - Return to main menu\n"
                "• *Cancel* - Cancel current operation\n"
                "• *Help* - Show this message"
            )
        else:
            return (
                "❓ *مساعدة*\n\n"
                "الأوامر المتاحة:\n"
                "• *القائمة* - العودة للقائمة الرئيسية\n"
                "• *إلغاء* - إلغاء العملية الحالية\n"
                "• *مساعدة* - عرض هذه الرسالة"
            )
    
    def get_invalid_selection_message(self, lang: str) -> str:
        """Invalid selection message"""
        if lang == "fr":
            return (
                "❌ Choix invalide. Veuillez sélectionner une option valide.\n\n"
                "💡 Tapez *Menu* pour recommencer"
            )
        elif lang == "en":
            return (
                "❌ Invalid selection. Please select a valid option.\n\n"
                "💡 Type *Menu* to start over"
            )
        else:
            return (
                "❌ اختيار غير صالح. المرجو اختيار خيار صحيح.\n\n"
                "💡 اكتب *القائمة* للبدء من جديد"
            )

    def get_insufficient_balance_message(self, lang: str) -> str:
        """Insufficient balance message"""
        if lang == "fr":
            return (
                "❌ Solde insuffisant pour effectuer cette opération.\n\n"
                "💡 Veuillez alimenter votre compte WafR."
            )
        elif lang == "en":
            return (
                "❌ Insufficient balance for this operation.\n\n"
                "💡 Please top up your WafR account."
            )
        else:
            return (
                "❌ رصيد غير كاف لإجراء هذه العملية.\n\n"
                "💡 المرجو تعبئة حسابكم في وفر."
            )
