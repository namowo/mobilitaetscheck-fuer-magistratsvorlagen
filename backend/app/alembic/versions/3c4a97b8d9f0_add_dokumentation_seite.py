"""add dokumentation_seite

Revision ID: 3c4a97b8d9f0
Revises: c6d7e8f9a0b1
Create Date: 2026-09-22 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3c4a97b8d9f0'
down_revision: Union[str, None] = 'c6d7e8f9a0b1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


GRUNDBAUSTEINE_INHALT = """<p>Diese Seite erklärt die zentralen Konzepte und Objekte, mit denen im Mobilitätscheck für Magistratsvorlagen gearbeitet wird.</p>
<h3>Magistratsvorlage</h3>
<p>Eine <strong>Magistratsvorlage</strong> ist das zentrale Arbeitsobjekt der Plattform. Sie entspricht einem kommunalen Vorhaben oder einer Entscheidungsvorlage, die in einem politischen Gremium (z.&nbsp;B. Stadtrat, Magistrat) beraten wird. Zu jeder Magistratsvorlage können ein oder mehrere Mobilitäts- und/oder Klimachecks erstellt werden.</p>
<h3>Mobilitätscheck</h3>
<p>Der <strong>Mobilitätscheck</strong> dient als sachliche Diskussionsgrundlage eines Vorhabens. So können (Teil-)Vorhaben mit verkehrlichen Leitzielen der Kommune gegenübergestellt werden. Bei Bedarf können ein allumfassender Mobilitätscheck oder mehrere Mobilitätschecks für Teilvorhaben einer Magistratsvorlage erstellt werden. Der Mobilitätscheck baut auf einem zweistufigen Zielsystem auf. Dabei wird betrachtet, ob die Ober- und dazugehörigen Unterziele von dem Vorhaben tangiert werden. Wenn ja, dann werden bei den Unterzielen weiterführende Angaben zu Wirkungsstärke und -Richtung, räumlichen Auswirkung, eine textliche Erläuterung sowie Indikatoren angegeben. Das Ergebnis kann als PDF exportiert und einer Magistratsvorlage beigelegt werden.</p>
<p>Initial wird der Mobilitätscheck von Verwaltungsmitarbeitenden ausgefüllt, veröffentlicht und als PDF der Magistratsvorlage beigefügt. Im nächsten Schritt können Kommunalpolitiker:innen den Mobilitätscheck in der Webanwendung einsehen, duplizieren und bearbeiten. Sie können ebenfalls die Mobilitätschecks veröffentlichen. Alle veröffentlichten Mobilitätschecks sind für die Allgemeinheit ohne Anmeldung aufruf- und einsehbar.</p>
<img src="/dokumentation/schema.png" alt="Schematischer Aufbau des Mobilitätschecks für Magistratsvorlagen">
<h4>Leitziele</h4>
<p><strong>Leitziele</strong> sind politisch legitimierte Ziele einer Kommune im Bereich Mobilität. Sie bilden die inhaltliche Grundlage des Mobilitätschecks: Jedes Vorhaben wird daraufhin bewertet, wie es sich auf die einzelnen Leitziele auswirkt. Leitziele können öffentlich gemacht werden, sodass neue Kommunen sich an bereits vorhandene Leitzielsysteme orientieren können. Die Leitziele müssen für den Mobilitätscheck zweistufig in Ober- und Unterziele differenziert werden.</p>
<p><strong>Oberziele</strong> sind übergeordnete Zielsetzungen. Beim Mobilitätscheck wird lediglich betrachtet, ob das Oberziel inhaltlich tangiert wird.</p>
<p><strong>Unterziele</strong> konkretisieren das zugehörige Oberziel und leiten sich aus diesem ab. Zunächst wird geschaut, ob das jeweilige Unterziel inhaltlich tangiert wird. Wenn ja, dann müssen weitere Angaben gemacht werden:</p>
<ol>
<li>Wirkungsrichtung- und Stärke gibt an, ob sich das Vorhaben positiv oder negativ sowie mit welcher Stärke auf das Unterziel auswirkt.</li>
<li>Die räumliche Auswirkung gibt an, ob das Vorhaben sich lokal, quartiers- oder stadtweit auf das Unterziel auswirkt.</li>
<li>Zudem kann eine schriftliche Erläuterung hinterlegt werden.</li>
<li>Indikatoren dienen als Beleg für die schriftliche Erläuterung. Hier kann auf Regelwerke, Studien oder messbare Kennwerte hingewiesen werden.</li>
</ol>
<h3>Textbausteine</h3>
<p><strong>Textbausteine</strong> sind vordefinierte Texte, die beim Ausfüllen eines Mobilitätschecks als Vorlage verwendet werden können. Sie helfen dabei, häufig wiederkehrende Formulierungen einheitlich und effizient einzusetzen. Textbausteine stehen ausschließlich Verwaltungsmitarbeitenden zur Verfügung und können interkommunal geteilt werden, um Synergieeffekte zu nutzen.</p>
<h4>Indikatoren</h4>
<p><strong>Indikatoren</strong> sind Regelwerke, Studien oder messbare Kennwerte, auf die sich die Erläuterung zur Auswirkung des Vorhabens auf ein Unterziel bezieht. Sie konkretisieren die Leitziele und machen die Bewertung im Mobilitätscheck nachvollziehbar und vergleichbar. Indikatoren können von Verwaltungsmitarbeitenden gepflegt und können interkommunal geteilt werden.</p>
<h4>Tags</h4>
<p><strong>Tags</strong> sind frei wählbare Schlagwörter zur Kategorisierung von Magistratsvorlagen, Indikatoren und anderen Objekten. Sie erleichtern das Filtern und Suchen innerhalb der Plattform. Tags werden von Verwaltungsmitarbeitenden gepflegt und können interkommunal geteilt werden.</p>
<h3>Klimacheck</h3>
<p>Der <strong>Klimacheck</strong> bewertet die Klimaauswirkungen eines Vorhabens. Sie ist ausschließlich für Verwaltungsmitarbeitende zugänglich und nicht für Politik oder die Öffentlichkeit sichtbar. Wie der Mobilitätscheck wird sie zu einer Magistratsvorlage erstellt und dient der internen Bewertung.</p>
<p>Der Klimacheck basiert auf der Arbeit des Klimaschutzmanagements der Stadt Oberursel (Taunus).</p>
<h3>Gruppen</h3>
<p><strong>Gruppen</strong> sind Benutzergruppen innerhalb einer Kommune. Sie ermöglichen es, Verwaltungsmitarbeitende und Kommunalpolitiker:innen zu organisieren und Zugriffsrechte strukturiert zu vergeben. Auf der Verwaltungsebene können User in Abteilungen oder Dezernate gruppiert werden. Auf der Politikebene können User in Fraktionen oder Parteien gegliedert werden. Gruppen werden von kommunalen Administratoren verwaltet. User können ihre Gruppe eigenständig einstellen.</p>
<h3>Gebiete</h3>
<p><strong>Gebiete</strong> sind Stadtgebiete und Ortsteile einer Gemeinde. Sie werden im Mobilitätscheck verwendet, um ein Vorhaben räumlich einzuordnen. Kommunale Administratoren pflegen die Liste der Gebiete im Einstellungsbereich.</p>"""

VERWALTUNG_INHALT = """<p>Verwaltungsmitarbeitende erstellen Magistratsvorlagen und führen dazu Mobilitäts- und Klimachecks durch.</p>
<h3>Benutzerrollen in der Verwaltung</h3>
<p>Innerhalb der Verwaltung wird zwischen einfachen Benutzern und Administratoren unterschieden.</p>
<h4>Kommunaler Administrator</h4>
<p>Ein kommunaler Administrator ist immer ein User aus der Verwaltung. Er hat zusätzlich Zugriff auf den gesamten <strong>Einstellungsbereich</strong> der eigenen Kommune:</p>
<ul>
<li><strong>Accountverwaltung</strong> – Benutzerkonten der eigenen Kommune einsehen, Rollen und Gruppen zuweisen, Benutzer löschen</li>
<li><strong>Einladungen</strong> – Einladungslinks erstellen und verwalten</li>
<li><strong>Gruppen</strong> – Benutzergruppen innerhalb der Gemeinde anlegen und verwalten (z.&nbsp;B. nach Fachbereich)</li>
<li><strong>Gebiete</strong> – Stadtgebiete und Ortsteile der Gemeinde pflegen, die im Mobilitätscheck verwendet werden</li>
<li><strong>Leitziele</strong> – Leitziel-Sets anlegen und verwalten, die dem Mobilitätscheck zugrunde liegen</li>
<li><strong>Textbausteine</strong> – Vordefinierte Textbausteine für den Mobilitätscheck erstellen und bearbeiten</li>
<li><strong>Indikatoren</strong> – Indikatoren pflegen, die zur Bewertung im Mobilitätscheck verwendet werden</li>
<li><strong>Tags</strong> – Tags für die Kategorisierung von Magistratsvorlagen, Indikatoren und Tags verwalten</li>
</ul>
<h4>Verwaltung (einfacher Benutzer)</h4>
<p>Ein einfacher Verwaltungsbenutzer kann:</p>
<ul>
<li>Magistratsvorlagen anlegen, bearbeiten und löschen</li>
<li>Mobilitätschecks zu Magistratsvorlagen erstellen, bearbeiten und als PDF exportieren</li>
<li>Klimachecks zu Magistratsvorlagen erstellen und bearbeiten</li>
<li>Andere Personen per E-Mail zur Verwaltung einladen (Einladungslink versenden)</li>
</ul>
<h3>Registrierung und erster Login</h3>
<p>Die Registrierung als Verwaltungsmitarbeitender erfolgt ausschließlich auf Einladung der dienstlichen E-Mail-Adresse.</p>
<h4>Registrierung als erster kommunaler Administrator</h4>
<ol>
<li>Kontaktieren Sie den Systemadministrator und bitten Sie darum, dass ihre Kommune hinzugefügt wird und Sie eine Einladung erhalten. Siehe dazu auch die Seite <em>Wie wird meine Kommune hinzugefügt?</em>.</li>
<li>Klicken Sie auf den Link in der Einladungsmail und folgen Sie den Anweisungen.</li>
<li>Sie sollten eine Bestätigungsmail erhalten haben. Bestätigen Sie ihren Account. Nun stehen ihnen alle Funktionen der Webanwendung zur Verfügung.</li>
</ol>
<h4>Registrierung bei bestehender Instanz</h4>
<ol>
<li>Kontaktieren Sie einen kommunalen Administrator und bitten Sie darum, dass Sie eine Einladung erhalten.</li>
<li>Klicken Sie auf den Link in der Einladungsmail und folgen Sie den Anweisungen.</li>
<li>Sie sollten eine Bestätigungsmail erhalten haben. Bestätigen Sie ihren Account. Nun stehen ihnen alle Funktionen der Webanwendung zur Verfügung.</li>
</ol>
<h4>Einladungen versenden</h4>
<ol>
<li>Klicken Sie oben rechts auf das Zahnrad (<strong>Einstellungen</strong>) und wählen Sie <strong>Einladungen</strong> in der linken Navigationsleiste aus. Hier können Sie weitere Verwaltungsmitarbeitende einladen.</li>
<li>Wählen Sie die entsprechende Benutzerrolle aus.</li>
<li>Kommunale Administratoren können weitere kommunale Administratoren ernennen, indem <strong>Als kommunaler Administrator einladen</strong> ausgewählt wird.</li>
<li>Geben Sie die E-Mail-Adresse der einzuladenden Person an.</li>
</ol>
<h3>Einrichtung</h3>
<p>Bevor Mobilitätschecks sinnvoll genutzt werden können, sollte ein kommunaler Administrator die folgenden Einstellungen vornehmen. Die Einstellungen sind über das Zahnrad-Symbol oben rechts erreichbar.</p>
<h4>Leitziele</h4>
<p>Leitziele sind das inhaltliche Herzstück des Mobilitätschecks. Sie definieren, welche verkehrspolitischen Ziele eine Kommune verfolgt, und werden bei der Bewertung von Magistratsvorlagen verwendet.</p>
<p>Leitziele sind in <strong>Leitziel-Sets</strong> organisiert. Ein Set enthält eine Sammlung von <strong>Oberzielen</strong>, denen jeweils mehrere <strong>Unterziele</strong> untergeordnet sind.</p>
<p><strong>Neues Leitziel-Set erstellen</strong></p>
<ol>
<li>Navigieren Sie in den Einstellungen zu <strong>Leitziele</strong>.</li>
<li>Klicken Sie auf <strong>Neue Leitziele erstellen</strong>.</li>
<li>Vergeben Sie einen Namen und optional eine Beschreibung.</li>
<li>Wählen Sie, ob das Set <strong>öffentlich sichtbar</strong> für andere Kommunen sein soll. Öffentliche Sets können von anderen Kommunen als Vorlage übernommen werden.</li>
<li>Fügen Sie Oberziele und die zugehörigen Unterziele hinzu.</li>
</ol>
<p><strong>Standard-Leitziele festlegen</strong></p>
<p>Ein Set kann als <strong>Standard</strong> markiert werden (Stern-Symbol). Das Standard-Set wird beim Erstellen neuer Mobilitätschecks automatisch vorausgewählt. Mindestens ein Standard-Set muss konfiguriert sein, bevor Mobilitätschecks erstellt werden können.</p>
<p><strong>Leitziele anderer Kommunen übernehmen</strong></p>
<p>Im Reiter <strong>Weitere Leitziele</strong> werden öffentliche Sets anderer Kommunen angezeigt. Mit <strong>Übernehmen</strong> wird eine eigene Kopie des Sets erstellt, die anschließend bearbeitet werden kann.</p>
<blockquote><strong>Hinweis:</strong> Änderungen an Leitzielen wirken sich auf alle bestehenden Mobilitätschecks aus, die auf diesem Set basieren. Werden Ober- oder Unterziele gelöscht, entfallen sie auch in bereits erstellten Mobilitätschecks. Für Tests empfiehlt es sich, ein Set zunächst zu duplizieren und die Änderungen an der Kopie vorzunehmen.</blockquote>
<h4>Gruppen</h4>
<p>Gruppen ermöglichen es, Benutzer innerhalb der Verwaltung und der Kommunalpolitik zu organisieren (z.&nbsp;B. nach Fachbereich oder Ausschuss).</p>
<ol>
<li>Navigieren Sie in den Einstellungen zu <strong>Gruppen</strong>.</li>
<li>Wechseln Sie zum Reiter <strong>Verwaltung</strong> oder <strong>Politik</strong>, je nachdem für welche Benutzerrolle Sie Gruppen anlegen möchten.</li>
<li>Klicken Sie auf <strong>Neue Gruppe</strong> und vergeben Sie einen Namen.</li>
<li>Weisen Sie Benutzer einer Gruppe zu – entweder per Drag &amp; Drop oder über das Auswahlmenü beim Benutzer.</li>
</ol>
<h4>Gebiete</h4>
<p>Gebiete sind Stadtteile oder Ortsteile, die bei einer Magistratsvorlage angegeben werden können, um den räumlichen Bezug der Maßnahme zu kennzeichnen.</p>
<ol>
<li>Navigieren Sie in den Einstellungen zu <strong>Gebiete</strong>.</li>
<li>Klicken Sie auf <strong>Neues Gebiet hinzufügen</strong> und vergeben Sie einen Namen.</li>
<li>Die angelegten Gebiete stehen beim Erstellen und Bearbeiten von Magistratsvorlagen zur Auswahl.</li>
</ol>
<h4>Tags</h4>
<p>Tags dienen der Kategorisierung von Magistratsvorlagen und Indikatoren.</p>
<ol>
<li>Navigieren Sie in den Einstellungen zu <strong>Tags</strong>.</li>
<li>Klicken Sie auf das <strong>Plus-Symbol</strong> und vergeben Sie einen Namen für den neuen Tag.</li>
<li>Tags können optional als gemeindespezifisch veröffentlicht werden, sodass sie auch anderen Kommunen zur Verfügung stehen.</li>
</ol>
<h4>Textbausteine</h4>
<p>Textbausteine sind vordefinierte Texte, die beim Ausfüllen eines Mobilitätschecks als Erläuterung zu einem Unterziel eingefügt werden können.</p>
<ol>
<li>Navigieren Sie in den Einstellungen zu <strong>Textbausteine</strong>.</li>
<li>Klicken Sie auf das <strong>Plus-Symbol</strong> und erfassen Sie den gewünschten Text.</li>
<li>Im Mobilitätscheck kann über die Schaltfläche <strong>Textbaustein hinzufügen</strong> ein gespeicherter Baustein in das Erläuterungsfeld eingefügt werden.</li>
</ol>
<h4>Indikatoren</h4>
<p>Indikatoren sind Messgrößen oder Kennzahlen, die bei der Bewertung eines Unterziels im Mobilitätscheck referenziert werden können.</p>
<ol>
<li>Navigieren Sie in den Einstellungen zu <strong>Indikatoren</strong>.</li>
<li>Klicken Sie auf das <strong>Plus-Symbol</strong>.</li>
<li>Geben Sie eine <strong>Bezeichnung</strong> an. Optional können Sie eine <strong>Quellen-URL</strong> sowie <strong>Tags</strong> zur Kategorisierung hinzufügen.</li>
<li>Im Mobilitätscheck können einem Unterziel ein oder mehrere Indikatoren zugeordnet werden. Ist eine Quellen-URL hinterlegt, erscheint der Indikator im PDF-Export als klickbarer Link.</li>
</ol>
<h3>Profil</h3>
<p>Unter <strong>Profil</strong> (oben rechts im Menü) können Sie Ihre persönlichen Accountdaten einsehen und bearbeiten, z.&nbsp;B. Benutzerrolle oder Passwort.</p>
<h3>Arbeiten mit Magistratsvorlagen</h3>
<h4>Magistratsvorlage anlegen</h4>
<ol>
<li>Navigieren Sie zur Übersicht <strong>Magistratsvorlagen</strong> und klicken Sie auf <strong>Neue Magistratsvorlage</strong>.</li>
<li>Füllen Sie das Formular aus:
<ul>
<li><strong>Magistratsvorlagennummer</strong> – Die interne Nummer der Vorlage.</li>
<li><strong>Datum der Magistratssitzung</strong> – Das geplante oder tatsächliche Sitzungsdatum.</li>
<li><strong>Titel der Magistratsvorlage</strong> – Eine aussagekräftige Bezeichnung der Maßnahme.</li>
<li><strong>Gebiete</strong> – Optionale Auswahl von Stadtteilen oder Ortsteilen mit räumlichem Bezug.</li>
<li><strong>Tags</strong> – Optionale Kategorisierung über Tags.</li>
<li><strong>Beschreibung der Maßnahme</strong> – Freitext zur inhaltlichen Beschreibung.</li>
</ul>
</li>
<li>Klicken Sie auf <strong>Speichern</strong>.</li>
</ol>
<p>Zu jeder Magistratsvorlage können anschließend ein oder mehrere <strong>Mobilitätschecks</strong> sowie ein <strong>Klimacheck</strong> erstellt werden.</p>
<h4>Mobilitätscheck</h4>
<p>Der Mobilitätscheck bewertet, wie sich eine Maßnahme auf die verkehrspolitischen Leitziele der Kommune auswirkt.</p>
<p><strong>Mobilitätscheck erstellen</strong></p>
<ol>
<li>Öffnen Sie die Magistratsvorlage und navigieren Sie zum Reiter <strong>Mobilitätschecks</strong>.</li>
<li>Klicken Sie auf <strong>Neuer Mobilitätscheck</strong>.</li>
<li>Vergeben Sie einen <strong>Namen</strong> für den Check.</li>
<li>Wählen Sie das <strong>Leitziel-Set</strong> aus, auf dessen Grundlage bewertet werden soll. Das als Standard markierte Set ist vorausgewählt.</li>
<li>Klicken Sie auf <strong>Mobilitätscheck anlegen</strong>.</li>
</ol>
<p><strong>Mobilitätscheck ausfüllen</strong></p>
<p>Der Mobilitätscheck ist nach <strong>Oberzielen</strong> und <strong>Unterzielen</strong> gegliedert.</p>
<p><strong>Oberziele</strong></p>
<p>Für jedes Oberziel des gewählten Leitziel-Sets wird entschieden, ob die Maßnahme dieses Ziel <strong>tangiert</strong>. Aktivieren Sie den Schalter, wenn das Oberziel relevant ist.</p>
<p><strong>Unterziele</strong></p>
<p>Wird ein Oberziel als tangiert markiert, werden seine Unterziele sichtbar. Für jedes relevante Unterziel können folgende Angaben gemacht werden:</p>
<ul>
<li><strong>Tangiert</strong> – Schalter, ob dieses Unterziel betroffen ist.</li>
<li><strong>Wirkungsrichtung und -stärke</strong> – Schieberegler von −3 (stark negativ) bis +3 (stark positiv). Der Wert 0 steht für neutral.</li>
<li><strong>Räumliche Auswirkung</strong> – Auswahl zwischen lokal, quartiersweit und stadtweit.</li>
<li><strong>Erläuterung</strong> – Freitext zur Begründung der Bewertung. Über <strong>Textbaustein hinzufügen</strong> können gespeicherte Textbausteine eingefügt werden.</li>
<li><strong>Indikatoren</strong> – Auswahl von einem oder mehreren Indikatoren, die die Bewertung belegen.</li>
</ul>
<p>Änderungen werden automatisch gespeichert.</p>
<p><strong>Mobilitätscheck abschließen</strong></p>
<ul>
<li>Klicken Sie auf <strong>Speichern</strong>, um den Check abzuschließen.</li>
<li>Fertige Mobilitätschecks können als <strong>PDF exportiert</strong> und der Magistratsvorlage beigelegt werden.</li>
<li>Fertige Mobilitätschecks können <strong>veröffentlicht</strong> werden. Veröffentlichte Mobilitätschecks sind für die Kommunalpolitik und – je nach Einstellung – für die Öffentlichkeit sichtbar.</li>
</ul>
<h4>Klimacheck</h4>
<p>Der Klimacheck bewertet die Klimarelevanz einer Magistratsvorlage. Er ist ausschließlich für Verwaltungsmitarbeitende zugänglich und wird weder für die Kommunalpolitik noch für die Öffentlichkeit angezeigt.</p>
<p><strong>Klimacheck erstellen</strong></p>
<ol>
<li>Öffnen Sie die Magistratsvorlage und navigieren Sie zum Reiter <strong>Klimacheck</strong>.</li>
<li>Klicken Sie auf <strong>Neuen Klimacheck erstellen</strong>.</li>
<li>Vergeben Sie einen <strong>Namen</strong> für den Klimacheck.</li>
<li>Beantworten Sie die fünf <strong>Ausgangsfragen</strong>, um die Klimarelevanz der Maßnahme einzuordnen. Die Fragen schließen sich teilweise gegenseitig aus:
<ul>
<li><strong>Frage 1</strong> – Handelt es sich um eine physische Maßnahme, eine Beschaffung oder deren konkrete Planung? (z.&nbsp;B. Begrünung, Umbau, Baumaaßnahmen)</li>
<li><strong>Frage 2</strong> – Handelt es sich um eine Planung oder ein Konzept, das indirekt physische Maßnahmen nach sich zieht? (z.&nbsp;B. Bebauungsplan)</li>
<li><strong>Frage 3</strong> – Beeinflusst das Vorhaben das Verhalten der Bevölkerung oder kommunaler Mitarbeitender in Bezug auf Klimaaspekte? (z.&nbsp;B. Klima-Bildungskampagne)</li>
<li><strong>Frage 4</strong> – Handelt es sich um ein klimawirksames Vorhaben, das nicht in die bisherigen Kategorien passt? (z.&nbsp;B. Reisen)</li>
<li><strong>Frage 5</strong> – Ist die Maßnahme in keiner Weise klimawirksam? (z.&nbsp;B. Personaleinstellung, Wahlen) – schließt die Fragen 1–4 aus.</li>
</ul>
</li>
<li>Klicken Sie auf <strong>Weiter</strong>.</li>
</ol>
<p><strong>Fragebögen ausfüllen</strong></p>
<p>Je nachdem, welche Ausgangsfragen (1–4) als zutreffend markiert wurden, werden die entsprechenden <strong>Fragebögen A–D</strong> freigeschaltet:</p>
<ul>
<li><strong>Fragebogen A</strong> (zu Frage 1) – Detailfragen zur physischen Maßnahme.</li>
<li><strong>Fragebogen B</strong> (zu Frage 2) – Detailfragen zu indirekten physischen Auswirkungen, z.&nbsp;B. Bebauungsplan (PV-Pflicht, Gründachpflicht, Regenwasserbewirtschaftung, hitzepräventive Maßnahmen u.&nbsp;a.).</li>
<li><strong>Fragebogen C</strong> (zu Frage 3) – Detailfragen zu Verhaltensauswirkungen.</li>
<li><strong>Fragebogen D</strong> (zu Frage 4) – Detailfragen zu sonstigen klimawirksamen Vorhaben.</li>
</ul>
<p>Klicken Sie auf die Schaltfläche <strong>zum Fragebogen</strong>, um einen Fragebogen zu öffnen. Gespeicherte, aber noch nicht abgeschlossene Fragebögen werden gelb, fertig ausgefüllte grün angezeigt.</p>
<p>Die Ausgangsfragen können nachträglich über <strong>Fragen bearbeiten</strong> angepasst werden.</p>
<p><strong>Klimacheck abschließen</strong></p>
<p>Sobald alle freigeschalteten Fragebögen vollständig ausgefüllt sind, kann der Klimacheck als <strong>PDF exportiert</strong> werden.</p>"""

POLITIK_INHALT = """<p>Mandatsträgerinnen und Mandatsträger können sich eigenständig registrieren, veröffentlichte Mobilitätschecks der Verwaltung einsehen und eigene Kopien zur Bearbeitung erstellen.</p>
<h3>Registrierung und erster Login</h3>
<ol>
<li>Registrieren Sie sich mit Ihrer E-Mail-Adresse. Wählen Sie <strong>Politik</strong> als Benutzerrolle aus.</li>
<li>Nach der Registrierung erhalten Sie eine E-Mail mit einem Bestätigungslink. Klicken Sie darauf, um Ihre Registrierung abzuschließen.</li>
<li>Nach der Bestätigung können Sie sich sofort anmelden – eine Freischaltung durch die Verwaltung ist nicht erforderlich.</li>
</ol>
<h3>Was können Sie als Kommunalpolitik tun?</h3>
<h4>Mobilitätschecks einsehen</h4>
<p>In der Übersicht <strong>Mobilitätschecks</strong> sehen Sie alle von der Verwaltung veröffentlichten Mobilitätschecks. Sie können diese einsehen und als PDF exportieren.</p>
<h4>Eigene Kopie erstellen</h4>
<p>Sie können jeden veröffentlichten Mobilitätscheck der Verwaltung <strong>duplizieren</strong>. Die Kopie gehört Ihnen und kann unabhängig bearbeitet werden. So können Sie eigene Einschätzungen und Bewertungen vornehmen, ohne den Original-Check der Verwaltung zu verändern.</p>
<ol>
<li>Öffnen Sie den gewünschten Mobilitätscheck.</li>
<li>Klicken Sie auf <strong>Duplizieren</strong>.</li>
<li>Bearbeiten Sie Ihre Kopie nach eigenen Vorstellungen.</li>
<li>Exportieren Sie den bearbeiteten Mobilitätscheck als <strong>PDF</strong>, um ihn mit anderen Mandatsträgerinnen und -trägern oder der Verwaltung zu teilen.</li>
</ol>
<h3>Was ist nicht zugänglich?</h3>
<p>Für Kommunalpolitiker ist es nicht möglich, Anpassungen am Leitzielsystem der Kommune vorzunehmen.</p>
<p>Klimachecks sind ausschließlich für die Verwaltung zugänglich und werden in der Ansicht der Kommunalpolitik nicht angezeigt.</p>"""

OEFFENTLICHER_ZUGANG_INHALT = """<p>Die Öffentlichkeit kann alle von der Verwaltung veröffentlichten Mobilitätschecks einsehen – ohne Registrierung und ohne Anmeldung.</p>
<h3>Zugang</h3>
<p>Rufen Sie die Anwendung auf und navigieren Sie zur öffentlichen Übersicht der Mobilitätschecks. Dort sind alle veröffentlichten Mobilitätschecks der teilnehmenden Kommunen aufgelistet und können direkt eingesehen werden.</p>
<p>Ein Benutzerkonto ist dafür nicht erforderlich.</p>
<h3>Was ist nicht zugänglich?</h3>
<ul>
<li>Das Erstellen, Bearbeiten oder Duplizieren von Mobilitätschecks ist ohne Anmeldung nicht möglich.</li>
<li>Klimachecks sind ausschließlich für die Verwaltung zugänglich.</li>
</ul>"""

KOMMUNE_HINZUFUEGEN_INHALT = """<p>Ihre Kommune nutzt den Mobilitätscheck für Magistratsvorlagen noch nicht? Damit Sie oder Kolleginnen und Kollegen sich als Verwaltung oder Kommunalpolitik registrieren können, muss die Kommune zunächst auf der Plattform angelegt werden.</p>
<h3>Ablauf</h3>
<ol>
<li>Nehmen Sie über den Kontakt-Button unten auf dieser Seite Kontakt mit dem Systemadministrator der Instanz auf und bitten Sie darum, dass Ihre Kommune hinzugefügt wird.</li>
<li>Der Systemadministrator legt die Kommune an und lädt eine erste Person als kommunalen Administrator ein.</li>
<li>Nach Annahme der Einladung kann der kommunale Administrator weitere Verwaltungsmitarbeitende einladen. Kommunalpolitiker:innen können sich anschließend selbst registrieren.</li>
</ol>
<p>Nähere Informationen zur Registrierung finden Sie auf der Seite <em>Verwaltung</em>.</p>"""


def upgrade() -> None:
    op.create_table(
        "dokumentation_seite",
        sa.Column("id", sa.Integer(), primary_key=True, index=True, nullable=False, comment="Dokumentationsseite ID"),
        sa.Column("titel", sa.Text(), nullable=False, comment="Titel der Dokumentationsseite"),
        sa.Column("slug", sa.Text(), nullable=False, comment="Eindeutiger Anker-Slug der Seite"),
        sa.Column("inhalt", sa.Text(), nullable=True, comment="Rich-Text-Inhalt der Dokumentationsseite (HTML)"),
        sa.Column("reihenfolge", sa.Integer(), nullable=False, server_default="0", comment="Anzeigereihenfolge der Seite"),
    )
    op.create_unique_constraint("uq_dokumentation_seite_slug", "dokumentation_seite", ["slug"])

    dokumentation_seite = sa.table(
        "dokumentation_seite",
        sa.column("titel", sa.Text()),
        sa.column("slug", sa.Text()),
        sa.column("inhalt", sa.Text()),
        sa.column("reihenfolge", sa.Integer()),
    )
    op.bulk_insert(
        dokumentation_seite,
        [
            {
                "titel": "Grundbausteine",
                "slug": "grundbausteine",
                "inhalt": GRUNDBAUSTEINE_INHALT,
                "reihenfolge": 0,
            },
            {
                "titel": "Verwaltung",
                "slug": "verwaltung",
                "inhalt": VERWALTUNG_INHALT,
                "reihenfolge": 1,
            },
            {
                "titel": "Kommunalpolitik",
                "slug": "politik",
                "inhalt": POLITIK_INHALT,
                "reihenfolge": 2,
            },
            {
                "titel": "Öffentlicher Zugang",
                "slug": "oeffentlicher-zugang",
                "inhalt": OEFFENTLICHER_ZUGANG_INHALT,
                "reihenfolge": 3,
            },
            {
                "titel": "Wie wird meine Kommune hinzugefügt?",
                "slug": "kommune-hinzufuegen",
                "inhalt": KOMMUNE_HINZUFUEGEN_INHALT,
                "reihenfolge": 4,
            },
        ],
    )


def downgrade() -> None:
    op.drop_table("dokumentation_seite")
