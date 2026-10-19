# Bayrak ve Dil Simgeleri Kuralı (Country Flags & Language Icons Rule)

Windows işletim sisteminde (Segoe UI Emoji font kısıtlaması nedeniyle) standart Unicode ülke bayrağı emojileri (🇹🇷, 🇬🇧, 🇺🇸 vb.) renkli bayrak olarak gösterilmez; onun yerine "TR", "GB", "US" şeklinde düz harfler olarak render edilir.

Bu sebeple kullanıcıya veya projelere metin, doküman veya arayüz üretirken:

1. **ASLA doğrudan Unicode bayrak emojisi (`🇹🇷`, `🇬🇧` vb.) kullanma.**
2. Markdown dosyalarında (README, CHANGELOG vb.), GitHub Actions Release notlarında ve web/UI sayfalarında her zaman evrensel olarak kusursuz render edilen görsel bayrakları kullan:
   - **Türkçe (TR):** `<img src="https://flagcdn.com/20x15/tr.png" width="20" height="15" alt="TR" valign="middle" /> Türkçe`
   - **İngilizce (GB):** `<img src="https://flagcdn.com/20x15/gb.png" width="20" height="15" alt="GB" valign="middle" /> English`
   - Genel format: `<img src="https://flagcdn.com/20x15/{kod}.png" width="20" height="15" alt="{KOD}" valign="middle" />`
3. Bu kural istisnasız tüm projelerde, sürümlerde ve dosyalarda geçerlidir.
