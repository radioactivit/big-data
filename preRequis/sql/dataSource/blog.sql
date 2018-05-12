-- Tables
CREATE TABLE Article (
	id INT UNSIGNED AUTO_INCREMENT,
	titre VARCHAR(200) NOT NULL,
	resume TEXT,
	contenu TEXT NOT NULL,
	auteur_id INT UNSIGNED NOT NULL,
	date_publication DATETIME NOT NULL,
	PRIMARY KEY(id)
);

CREATE TABLE Utilisateur (
	id INT UNSIGNED AUTO_INCREMENT,
	pseudo VARCHAR(100) NOT NULL,
	email VARCHAR(200) NOT NULL,
	password CHAR(40) NOT NULL,  -- le mot de passe sera hashé avec sha1, ce qui donne toujours une chaîne de 40 caractères
	PRIMARY KEY(id)
);

CREATE TABLE Categorie (
	id INT UNSIGNED AUTO_INCREMENT,
	nom VARCHAR(150) NOT NULL,
	PRIMARY KEY(id)
);

CREATE TABLE Categorie_article (
	categorie_id INT UNSIGNED,
	article_id INT UNSIGNED,
	PRIMARY KEY (categorie_id, article_id)
);

CREATE TABLE Commentaire (
	id INT UNSIGNED AUTO_INCREMENT,
	article_id INT UNSIGNED NOT NULL,
	auteur_id INT UNSIGNED,
	contenu TEXT NOT NULL,
	date_commentaire DATETIME NOT NULL,
	PRIMARY KEY(id)
);

-- Clés étrangères
ALTER TABLE Article 
ADD CONSTRAINT fk_auteur_article FOREIGN KEY (auteur_id) REFERENCES Utilisateur(id);

ALTER TABLE Categorie_article 
ADD CONSTRAINT fk_article_cat FOREIGN KEY (article_id) REFERENCES Article(id),
ADD CONSTRAINT fk_categorie_cat FOREIGN KEY (categorie_id) REFERENCES Categorie(id);

ALTER TABLE Commentaire  
ADD CONSTRAINT fk_article_com FOREIGN KEY (article_id) REFERENCES Article(id),
ADD CONSTRAINT fk_auteur_com FOREIGN KEY (auteur_id) REFERENCES Utilisateur(id);

-- Index
CREATE UNIQUE INDEX unique_email
ON Utilisateur(email);

CREATE UNIQUE INDEX unique_pseudo
ON Utilisateur(pseudo);

CREATE INDEX index_date_article 
ON Article(date_publication);

CREATE INDEX index_date_commentaire
ON Commentaire(date_commentaire);


-- Insertion d'utilisateurs

INSERT INTO Utilisateur (pseudo, email, password) VALUES
('Baudelaire', 'baudelaire@email.com', '6fd4c29cbd6a758bce1acf991aa9f32e69ced155'),
('Rimbaud', 'rimbaud@email.com', '6fd4c29cbd6a758bce1acf991aa9f32e69ced155'),
('Victor Hugo', 'vhugo@email.com', '3edb6ce6e328ea8639a3a357c7c6997775ab52ea'),
('JacquesP', 'j.prevert@email.com', '713f55ba75af01593dc4e845a8c0dcb9fbb45a88');

-- Insertion de categories

INSERT INTO Categorie (nom) VALUES
('Guerre'),
('Mélancolie'),
('Amour'),
('Mort'),
('Saison');

-- Insertion d'articles

INSERT INTO Article (titre, resume, contenu, auteur_id, date_publication) VALUES
('Confession', 'Une fois, une seule, aimable et douce femme,\r\nA mon bras votre bras poli\r\nS''appuya (sur le fond ténébreux de mon âme\r\nCe souvenir n''est point pâli) ;', 'Une fois, une seule, aimable et douce femme,\r\nA mon bras votre bras poli\r\nS''appuya (sur le fond ténébreux de mon âme\r\nCe souvenir n''est point pâli) ;\r\n\r\nIl était tard ; ainsi qu''une médaille neuve\r\nLa pleine lune s''étalait,\r\nEt la solennité de la nuit, comme un fleuve,\r\nSur Paris dormant ruisselait.\r\n\r\nEt le long des maisons, sous les portes cochères,\r\nDes chats passaient furtivement,\r\nL''oreille au guet, ou bien, comme des ombres chères,\r\nNous accompagnaient lentement.\r\n\r\nTout à coup, au milieu de l''intimité libre\r\nÉclose à la pâle clarté,\r\nDe vous, riche et sonore instrument où ne vibre\r\nQue la radieuse gaieté,\r\n\r\nDe vous, claire et joyeuse ainsi qu''une fanfare\r\nDans le matin étincelant,\r\nUne note plaintive, une note bizarre\r\nS''échappa, tout en chancelant\r\n\r\nComme une enfant chétive, horrible, sombre, immonde,\r\nDont sa famille rougirait,\r\nEt qu''elle aurait longtemps, pour la cacher au monde,\r\nDans un caveau mise au secret.\r\n\r\nPauvre ange, elle chantait, votre note criarde :\r\n" Que rien ici-bas n''est certain,\r\nEt que toujours, avec quelque soin qu''il se farde,\r\nSe trahit l''égoïsme humain ;\r\n\r\nQue c''est un dur métier que d''être belle femme,\r\nEt que c''est le travail banal\r\nDe la danseuse folle et froide qui se pâme\r\nDans un sourire machinal ;\r\n\r\nQue bâtir sur les coeurs est une chose sotte ;\r\nQue tout craque, amour et beauté,\r\nJusqu''à ce que l''Oubli les jette dans sa hotte\r\nPour les rendre à l''Éternité ! "\r\n\r\nJ''ai souvent évoqué cette lune enchantée,\r\nCe silence et cette langueur,\r\nEt cette confidence horrible chuchotée\r\nAu confessionnal du coeur.', 1, '2014-10-20 14:43:07'),
('Sonnet d''automne', 'Ils me disent, tes yeux, clairs comme le cristal :\r\n" Pour toi, bizarre amant, quel est donc mon mérite ? "\r\n- Sois charmante et tais-toi ! Mon coeur, que tout irrite,\r\nExcepté la candeur de l''antique animal,\r\n\r\nNe veut pas te montrer son secret infernal,\r\nBerceuse dont la main aux longs sommeils m''invite,\r\nNi sa noire légende avec la flamme écrite.\r\nJe hais la passion et l''esprit me fait mal !\r\n\r\nAimons-nous doucement. L''Amour dans sa guérite,\r\nTénébreux, embusqué, bande son arc fatal.\r\nJe connais les engins de son vieil arsenal :\r\n\r\nCrime, horreur et folie ! - Ô pâle marguerite !\r\nComme moi n''es-tu pas un soleil automnal,\r\nÔ ma si blanche, ô ma si froide Marguerite ?', 'Ils me disent, tes yeux, clairs comme le cristal :\r\n" Pour toi, bizarre amant, quel est donc mon mérite ? "\r\n- Sois charmante et tais-toi ! Mon coeur, que tout irrite,\r\nExcepté la candeur de l''antique animal,\r\n\r\nNe veut pas te montrer son secret infernal,\r\nBerceuse dont la main aux longs sommeils m''invite,\r\nNi sa noire légende avec la flamme écrite.\r\nJe hais la passion et l''esprit me fait mal !\r\n\r\nAimons-nous doucement. L''Amour dans sa guérite,\r\nTénébreux, embusqué, bande son arc fatal.\r\nJe connais les engins de son vieil arsenal :\r\n\r\nCrime, horreur et folie ! - Ô pâle marguerite !\r\nComme moi n''es-tu pas un soleil automnal,\r\nÔ ma si blanche, ô ma si froide Marguerite ?', 1, '2014-10-24 16:38:23'),
('Le dormeur du val', 'C''est un trou de verdure où chante une rivière,\r\nAccrochant follement aux herbes des haillons\r\nD''argent ; où le soleil, de la montagne fière,\r\nLuit : c''est un petit val qui mousse de rayons.', 'C''est un trou de verdure où chante une rivière,\r\nAccrochant follement aux herbes des haillons\r\nD''argent ; où le soleil, de la montagne fière,\r\nLuit : c''est un petit val qui mousse de rayons.\r\n\r\nUn soldat jeune, bouche ouverte, tête nue,\r\nEt la nuque baignant dans le frais cresson bleu,\r\nDort ; il est étendu dans l''herbe, sous la nue,\r\nPâle dans son lit vert où la lumière pleut.\r\n\r\nLes pieds dans les glaïeuls, il dort. Souriant comme\r\nSourirait un enfant malade, il fait un somme :\r\nNature, berce-le chaudement : il a froid.\r\n\r\nLes parfums ne font pas frissonner sa narine ;\r\nIl dort dans le soleil, la main sur sa poitrine,\r\nTranquille. Il a deux trous rouges au côté droit.', 2, '2014-10-28 07:50:25'),
('Les corbeaux', 'Seigneur, quand froide est la prairie,\r\nQuand dans les hameaux abattus,\r\nLes longs angelus se sont tus...\r\nSur la nature défleurie\r\nFaites s''abattre des grands cieux\r\nLes chers corbeaux délicieux.', 'Seigneur, quand froide est la prairie,\r\nQuand dans les hameaux abattus,\r\nLes longs angelus se sont tus...\r\nSur la nature défleurie\r\nFaites s''abattre des grands cieux\r\nLes chers corbeaux délicieux.\r\n\r\nArmée étrange aux cris sévères,\r\nLes vents froids attaquent vos nids !\r\nVous, le long des fleuves jaunis,\r\nSur les routes aux vieux calvaires,\r\nSur les fossés et sur les trous\r\nDispersez-vous, ralliez-vous !\r\n\r\nPar milliers, sur les champs de France,\r\nOù dorment des morts d''avant-hier,\r\nTournoyez, n''est-ce pas, l''hiver,\r\nPour que chaque passant repense !\r\nSois donc le crieur du devoir,\r\nÔ notre funèbre oiseau noir !\r\n\r\nMais, saints du ciel, en haut du chêne,\r\nMât perdu dans le soir charmé,\r\nLaissez les fauvettes de mai\r\nPour ceux qu''au fond du bois enchaîne,\r\nDans l''herbe d''où l''on ne peut fuir,\r\nLa défaite sans avenir.', 2, '2014-10-06 07:07:42'),
('Demain dès l''aube', 'Demain, dès l''aube, à l''heure où blanchit la campagne,\r\nJe partirai. Vois-tu, je sais que tu m''attends.', 'Demain, dès l''aube, à l''heure où blanchit la campagne,\r\nJe partirai. Vois-tu, je sais que tu m''attends.\r\nJ''irai par la forêt, j''irai par la montagne.\r\nJe ne puis demeurer loin de toi plus longtemps.\r\n\r\nJe marcherai les yeux fixés sur mes pensées,\r\nSans rien voir au dehors, sans entendre aucun bruit,\r\nSeul, inconnu, le dos courbé, les mains croisées,\r\nTriste, et le jour pour moi sera comme la nuit.\r\n\r\nJe ne regarderai ni l''or du soir qui tombe,\r\nNi les voiles au loin descendant vers Harfleur,\r\nEt quand j''arriverai, je mettrai sur ta tombe\r\nUn bouquet de houx vert et de bruyère en fleur.', 3, '2014-10-30 22:25:30'),
('Après l''hiver', 'N''attendez pas de moi que je vais vous donner \r\nDes raisons contre Dieu que je vois rayonner ; \r\nLa nuit meurt, l''hiver fuit ; maintenant la lumière, \r\nDans les champs, dans les bois, est partout la première. \r\nJe suis par le printemps vaguement attendri. ', 'N''attendez pas de moi que je vais vous donner \r\nDes raisons contre Dieu que je vois rayonner ; \r\nLa nuit meurt, l''hiver fuit ; maintenant la lumière, \r\nDans les champs, dans les bois, est partout la première. \r\nJe suis par le printemps vaguement attendri. \r\nAvril est un enfant, frêle, charmant, fleuri ; \r\nJe sens devant l''enfance et devant le zéphyre \r\nJe ne sais quel besoin de pleurer et de rire ; \r\nMai complète ma joie et s''ajoute à mes pleurs. \r\nJeanne, George, accourez, puisque voilà des fleurs. \r\nAccourez, la forêt chante, l''azur se dore, \r\nVous n''avez pas le droit d''être absents de l''aurore. \r\nJe suis un vieux songeur et j''ai besoin de vous, \r\nVenez, je veux aimer, être juste, être doux, \r\nCroire, remercier confusément les choses, \r\nVivre sans reprocher les épines aux roses,\r\nÊtre enfin un bonhomme acceptant le bon Dieu.\r\n\r\nÔ printemps ! bois sacrés ! ciel profondément bleu ! \r\nOn sent un souffle d''air vivant qui vous pénètre, \r\nEt l''ouverture au loin d''une blanche fenêtre ;\r\nOn mêle sa pensée au clair-obscur des eaux ; \r\nOn a le doux bonheur d''être avec les oiseaux \r\nEt de voir, sous l''abri des branches printanières, \r\nCes messieurs faire avec ces dames des manières.', 3, '2014-10-20 05:07:45'),
('Le désespoir est assis sur un banc', 'Dans un square sur un banc\r\nIl y a un homme qui vous appelle quand on passe\r\nIl a des binocles un vieux costume gris\r\nIl fume un petit ninas il est assis\r\nEt il vous appelle quand on passe', 'Dans un square sur un banc\r\nIl y a un homme qui vous appelle quand on passe\r\nIl a des binocles un vieux costume gris\r\nIl fume un petit ninas il est assis\r\nEt il vous appelle quand on passe\r\nOu simplement il vous fait signe\r\nIl ne faut pas le regarder\r\nIl ne faut pas l''écouter\r\nIl faut passer\r\nFaire comme si on ne le voyait pas\r\nComme si on ne l''entendait pas\r\nIl faut passer et presser le pas\r\nSi vous le regardez\r\nSi vous l''écoutez\r\nIl vous fait signe et rien personne\r\nNe peut vous empêcher d''aller vous asseoir près de lui\r\nAlors il vous regarde et sourit\r\nEt vous souffrez atrocement\r\nEt l''homme continue de sourire\r\nEt vous souriez du même sourire\r\nExactement\r\nPlus vous souriez plus vous souffrez\r\nAtrocement\r\nPlus vous souffrez plus vous souriez\r\nIrrémédiablement\r\nEt vous restez là\r\nAssis figé\r\nSouriant sur le banc\r\nDes enfants jouent tout près de vous\r\nDes passants passent\r\nTranquillement\r\nDes oiseaux s''envolent\r\nQuittant un arbre\r\nPour un autre\r\nEt vous restez là\r\nSur le banc\r\nEt vous savez vous savez\r\nQue jamais plus vous ne jouerez\r\nComme ces enfants\r\nVous savez que jamais plus vous ne passerez\r\nTranquillement\r\nComme ces passants\r\nQue jamais plus vous ne vous envolerez\r\nQuittant un arbre pour un autre\r\nComme ces oiseaux.', 4, '2014-10-01 08:10:35'),
('Un beau matin', 'Il n''avait peur de personne \r\nIl n''avait peur de rien \r\nMais un matin un beau matin \r\nIl croit voir quelque chose ', 'Il n''avait peur de personne \r\nIl n''avait peur de rien \r\nMais un matin un beau matin \r\nIl croit voir quelque chose \r\nMais il dit Ce n''est rien \r\nEt il avait raison \r\nAvec sa raison sans nul doute \r\nCe n'' était rien \r\nMais le matin ce même matin \r\nIl croit entendre quelqu''un \r\nEt il ouvrit la porte \r\nEt il la referma en disant Personne \r\nEt il avait raison \r\nAvec sa raison sans nul doute \r\nIl n''y avait personne \r\nMais soudain il eut peur \r\nEt il comprit qu''Il était seul \r\nMais qu''Il n''était pas tout seul \r\nEt c''est alors qu''il vit \r\nRien en personne devant lui \r\n', 4, '2014-10-11 16:50:17');

-- Insertion categories-articles

INSERT INTO Categorie_article (categorie_id, article_id) VALUES
(2, 1),
(3, 1),
(3, 2),
(5, 2),
(1, 3),
(4, 3),
(2, 4),
(4, 4),
(3, 5),
(4, 5),
(5, 6),
(2, 7),
(2, 8);

-- Insertion de commentaires

INSERT INTO Commentaire (article_id, auteur_id, contenu, date_commentaire) VALUES
(1, 4, 'Mangifique', '2014-11-10 05:06:47'),
(1, NULL, 'Très joli', '2014-11-04 04:47:35'),
(2, NULL, 'J''ai pas tout compris...', '2014-11-14 06:34:30'),
(2, 2, 'Quel joli texte, j''adore !', '2014-11-05 23:07:52'),
(3, NULL, 'C''est gai tout ça...', '2014-11-26 05:42:04'),
(4, 1, 'Tellement beau, on ne s''en lasse pas.', '2014-11-23 07:44:33'),
(5, 1, 'Incroyable !!!', '2014-11-22 12:05:34'),
(5, 2, 'Pas mal, j''aime bien', '2014-11-24 08:47:15'),
(8, 1, 'Exceptionnel, mais un peu triste quand même...', '2014-11-15 21:56:05'),
(5, NULL, 'Mouais, pas convaincue...', '2014-11-09 09:09:09');

