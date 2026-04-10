from __future__ import annotations

from typing import List, Literal, Optional

from pydantic import BaseModel, Field, ConfigDict


class Claim(BaseModel):
    claim_id: str = Field(
        ...,
        description="Identifiant unique de l'allégation dans le document.",
    )
    claim_text: str = Field(
        ...,
        description="Texte de l'allégation telle qu'exprimée dans le document (FR/EN).",
    )
    claim_type: Literal[
        "event",
        "accusation",
        "denial",
        "responsibility",
        "casualty",
        "location",
        "identity",
        "other",
    ] = Field(
        ...,
        description=(
            "Catégorie d'allégation (événement, accusation, démenti, bilan, "
            "lieu, identité, etc.)."
        ),
    )
    stance: Literal["asserted", "alleged", "denied", "uncertain"] = Field(
        ...,
        description="Position de la source par rapport à l'allégation.",
    )


class EntityBlock(BaseModel):
    persons: List[str] = Field(
        default_factory=list,
        description=(
            "Noms de personnes mentionnées (tels que dans le texte, sans "
            "normalisation)."
        ),
    )
    organizations: List[str] = Field(
        default_factory=list,
        description="Organisations, institutions, entreprises, groupes armés, etc.",
    )
    locations: List[str] = Field(
        default_factory=list,
        description="Lieux mentionnés (villes, régions, bâtiments, etc.).",
    )
    dates: List[str] = Field(
        default_factory=list,
        description=(
            "Dates mentionnées dans le texte, au format original "
            "(pas besoin d’ISO)."
        ),
    )
    events: List[str] = Field(
        default_factory=list,
        description=(
            "Noms d’événements (manifestations, opérations militaires, "
            "élections...)."
        ),
    )
    handles: List[str] = Field(
        default_factory=list,
        description="Handles / comptes (ex: @username, @media_org).",
    )
    websites: List[str] = Field(
        default_factory=list,
        description="URLs ou noms de sites cités.",
    )


class GeoLocation(BaseModel):
    raw_text: Optional[str] = Field(
        None,
        description=(
            "Expression textuelle brute du lieu telle qu'apparait dans le document."
        ),
    )
    normalized_name: Optional[str] = Field(
        None,
        description="Nom géographique normalisé (si possible).",
    )
    country: Optional[str] = Field(
        None,
        description="Pays (ISO-3166 alpha-2 ou nom en toutes lettres).",
    )
    admin1: Optional[str] = Field(
        None,
        description=(
            "Subdivision administrative de premier niveau "
            "(gouvernorat, région, etc.)."
        ),
    )
    lat: Optional[float] = Field(
        None,
        description="Latitude approximative, si connue.",
    )
    lon: Optional[float] = Field(
        None,
        description="Longitude approximative, si connue.",
    )
    confidence: Optional[float] = Field(
        None,
        ge=0.0,
        le=1.0,
        description="Confiance (0.0–1.0) dans la géolocalisation proposée.",
    )


class CredibilityAssessment(BaseModel):
    label: Literal["high", "medium", "low", "unknown"] = Field(
        ...,
        description="Appréciation globale de crédibilité de la source/document.",
    )
    score: int = Field(
        ...,
        ge=0,
        le=100,
        description="Score de crédibilité 0–100 (plus haut = plus crédible).",
    )
    rationale: str = Field(
        ...,
        description="Courte explication textuelle justifiant le label/score.",
    )
    evidence_present: List[str] = Field(
        default_factory=list,
        description=(
            "Types de preuves présentes (photos, vidéos, documents officiels, "
            "témoignages...)."
        ),
    )
    verification_status: Literal[
        "unverified",
        "partially_verified",
        "corroborated",
        "contradicted",
    ] = Field(
        ...,
        description="Statut de vérification globale.",
    )


class RedFlag(BaseModel):
    type: Literal[
        "no_source",
        "anonymous_origin",
        "date_mismatch",
        "location_mismatch",
        "image_reuse",
        "metadata_conflict",
        "sensational_language",
        "unsupported_claim",
        "other",
    ] = Field(
        ...,
        description="Type de signal d’alerte.",
    )
    span_text: str = Field(
        ...,
        description="Extrait du document illustrant ce red flag.",
    )
    explanation: str = Field(
        ...,
        description="Pourquoi cet extrait constitue un red flag.",
    )


class Classification(BaseModel):
    information_disorder: Literal[
        "official",
        "reporting",
        "rumor",
        "misinformation",
        "disinformation",
        "propaganda",
        "opinion",
        "unknown",
    ] = Field(
        ...,
        description="Catégorie d’information / désordre informationnel.",
    )
    topic: List[str] = Field(
        default_factory=list,
        description="Thèmes ou sujets (ex: elections, corruption, police_violence...).",
    )
    country: List[str] = Field(
        default_factory=list,
        description="Pays concernés (codes ISO ou noms).",
    )
    actor: List[str] = Field(
        default_factory=list,
        description="Acteurs principaux (personnes, organisations, États...).",
    )
    violation_type: List[str] = Field(
        default_factory=list,
        description=(
            "Types de violations (ex: human_rights, freedom_of_press, "
            "war_crime...)."
        ),
    )
    crime_type: List[str] = Field(
        default_factory=list,
        description=(
            "Types de crimes (ex: corruption, torture, enforced_disappearance...)."
        ),
    )


class OSINTDocument(BaseModel):
    document_id: str = Field(
        ...,
        description="Identifiant interne du document dans ton pipeline.",
    )
    language: Optional[str] = Field(
        None,
        description="Langue principale du document (ex: fr, en, ar).",
    )
    source_type: Literal[
        "official",
        "media",
        "social",
        "ngo",
        "company",
        "database",
        "anonymous",
        "other",
    ] = Field(
        ...,
        description="Type de source principale.",
    )
    source_name: Optional[str] = Field(
        None,
        description="Nom de la source (média, institution, compte, etc.).",
    )
    source_url: Optional[str] = Field(
        None,
        description="URL de la source ou du document si disponible.",
    )
    publication_date: Optional[str] = Field(
        None,
        description="Date de publication (ISO 8601 si possible).",
    )
    retrieval_date: Optional[str] = Field(
        None,
        description="Date à laquelle tu as récupéré le document.",
    )
    claims: List[Claim] = Field(
        default_factory=list,
        description="Liste des allégations extraites du document.",
    )
    entities: EntityBlock = Field(
        default_factory=EntityBlock,
        description="Bloc d'entités nommées extraites.",
    )
    geolocation: Optional[GeoLocation] = Field(
        default=None,
        description="Informations de géolocalisation principales, si déductibles.",
    )
    credibility_assessment: CredibilityAssessment = Field(
        ...,
        description="Évaluation de crédibilité du document.",
    )
    red_flags: List[RedFlag] = Field(
        default_factory=list,
        description="Liste des signaux d’alerte relevés dans le document.",
    )
    classification: Classification = Field(
        ...,
        description="Classification du document selon plusieurs dimensions.",
    )
    cross_reference_needs: List[str] = Field(
        default_factory=list,
        description="Ce qui nécessite une vérification/corroboration supplémentaire.",
    )
    output_version: str = Field(
        default="1.0",
        description="Version du schéma de sortie.",
    )

    model_config = ConfigDict(
        extra="ignore",
        title="OSINTDocument",
        json_schema_extra={
            "description": (
                "Sortie structurée pour l'analyse OSINT d'un document textuel."
            )
        },
    )