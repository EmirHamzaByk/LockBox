# Lock Box

Uygulama, kullanıcıların çeşitli web siteleri, kullanıcı adları ve şifrelerini saklamalarını ve güncellemelerini sağlar. Şifreler, SQLite veritabanı kullanılarak yerel bir dosyada saklanır.

**Kodun işleyişi aşağıdaki adımlardan oluşur:**

İlk olarak, Şifre sınıfı başlatılır ve veritabanı bağlantısı kurulur. Gerekli tablo oluşturulur ve ana uygulama penceresi tanımlanır.

Ana uygulama penceresi, kullanıcı adı, şifre ve web sitesi girişleri için gerekli etiketler ve giriş alanları oluşturulur. Şifre girişi, kullanıcının girdiğini görebilmesi için "Göster/Gizle" düğmesi ile kontrol edilebilir.

"Kaydet" düğmesine tıkladığında, kullanıcının girdiği veriler veritabanına eklenir ve mesaj kutusuyla başarılı bir şekilde kaydedildiği bildirilir.

"Kaydedilmiş Şifreleri Göster" düğmesi, uygulamanın ana penceresinin altına yerleştirilmiş olup, kullanıcının eklenen şifreleri listeleyen ayrı bir pencere açar.

Liste penceresi, kaydedilen şifreleri liste halinde gösterir ve her şifre için "Güncelle" ve "Sil" düğmeleri içerir.

"Güncelle" düğmesine tıklandığında, kullanıcı ilgili şifreyi güncellemek için yeni bir pencere açar ve değişiklikler veritabanında güncellenir.

"Sil" düğmesine tıklandığında, kullanıcı o şifreyi veritabanından silmek isteyip istemediğini onaylaması için bir iletişim kutusu görüntülenir. Onay verildiğinde, ilgili şifre veritabanından silinir.

Bu kod,  bir şifre yöneticisi uygulaması oluşturur ve kullanıcıların şifrelerini güvenli bir şekilde saklamalarına olanak tanır. Kullanıcı dostu arayüzü sayesinde, şifreleri kolayca eklemek, güncellemek ve silmek mümkündür.
