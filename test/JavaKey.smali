.class public Lit/uniroma2/adidiego/apikeytestapp/JavaKey;
.super Ljava/lang/Object;
.source "JavaKey.java"


# static fields
.field public static final API_KEY_FINAL_STATIC:Ljava/lang/String; = "GIzaSyCuxR_sUTfFJZBDkIsauakeuqXaFxhbur4"

.field public static final API_KEY_FINAL_STATIC_ARRAY:[Ljava/lang/String;

.field public static apiKeyStatic:Ljava/lang/String;

.field public static apiKeyStaticArray:[Ljava/lang/String;


# instance fields
.field private apiKeyPrivate:Ljava/lang/String;

.field private apiKeyPrivateArray:[Ljava/lang/String;

.field public apiKeyPublic:Ljava/lang/String;

.field public apiKeyPublicArray:[Ljava/lang/String;


# direct methods
.method static constructor <clinit>()V
    .locals 5

    .prologue
    const/4 v4, 0x2

    const/4 v3, 0x1

    const/4 v2, 0x0

    .line 13
    const-string v0, "FIzaSyCuxR_sUTfFJZBDkIsauakeuqXaFxhbur4"

    sput-object v0, Lit/uniroma2/adidiego/apikeytestapp/JavaKey;->apiKeyStatic:Ljava/lang/String;

    .line 14
    new-array v0, v4, [Ljava/lang/String;

    const-string v1, "TIzaSyCuxR_sUTfFJZBDkIsauakeuqXaFxhbur4"

    aput-object v1, v0, v2

    const-string v1, "UIzaSyCuxR_sUTfFJZBDkIsauakeuqXaFxhbur4"

    aput-object v1, v0, v3

    sput-object v0, Lit/uniroma2/adidiego/apikeytestapp/JavaKey;->apiKeyStaticArray:[Ljava/lang/String;

    .line 16
    new-array v0, v4, [Ljava/lang/String;

    const-string v1, "VIzaSyCuxR_sUTfFJZBDkIsauakeuqXaFxhbur4"

    aput-object v1, v0, v2

    const-string v1, "WIzaSyCuxR_sUTfFJZBDkIsauakeuqXaFxhbur4"

    aput-object v1, v0, v3

    sput-object v0, Lit/uniroma2/adidiego/apikeytestapp/JavaKey;->API_KEY_FINAL_STATIC_ARRAY:[Ljava/lang/String;

    return-void
.end method

.method public constructor <init>()V
    .locals 5

    .prologue
    const/4 v4, 0x2

    const/4 v3, 0x1

    const/4 v2, 0x0

    .line 7
    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    .line 9
    const-string v0, "DIzaSyCuxR_sUTfFJZBDkIsauakeuqXaFxhbur4"

    iput-object v0, p0, Lit/uniroma2/adidiego/apikeytestapp/JavaKey;->apiKeyPublic:Ljava/lang/String;

    .line 10
    new-array v0, v4, [Ljava/lang/String;

    const-string v1, "PIzaSyCuxR_sUTfFJZBDkIsauakeuqXaFxhbur4"

    aput-object v1, v0, v2

    const-string v1, "QIzaSyCuxR_sUTfFJZBDkIsauakeuqXaFxhbur4"

    aput-object v1, v0, v3

    iput-object v0, p0, Lit/uniroma2/adidiego/apikeytestapp/JavaKey;->apiKeyPublicArray:[Ljava/lang/String;

    .line 11
    const-string v0, "EIzaSyCuxR_sUTfFJZBDkIsauakeuqXaFxhbur4"

    iput-object v0, p0, Lit/uniroma2/adidiego/apikeytestapp/JavaKey;->apiKeyPrivate:Ljava/lang/String;

    .line 12
    new-array v0, v4, [Ljava/lang/String;

    const-string v1, "RIzaSyCuxR_sUTfFJZBDkIsauakeuqXaFxhbur4"

    aput-object v1, v0, v2

    const-string v1, "SIzaSyCuxR_sUTfFJZBDkIsauakeuqXaFxhbur4"

    aput-object v1, v0, v3

    iput-object v0, p0, Lit/uniroma2/adidiego/apikeytestapp/JavaKey;->apiKeyPrivateArray:[Ljava/lang/String;

    return-void
.end method


# virtual methods
.method public getGlobalPrivateKey()Ljava/lang/String;
    .locals 1

    .prologue
    .line 37
    iget-object v0, p0, Lit/uniroma2/adidiego/apikeytestapp/JavaKey;->apiKeyPrivate:Ljava/lang/String;

    return-object v0
.end method

.method public getGlobalPrivateKeyArray()[Ljava/lang/String;
    .locals 1

    .prologue
    .line 41
    iget-object v0, p0, Lit/uniroma2/adidiego/apikeytestapp/JavaKey;->apiKeyPrivateArray:[Ljava/lang/String;

    return-object v0
.end method

.method public getLocalKey()Ljava/lang/String;
    .locals 1

    .prologue
    .line 19
    const-string v0, "BIzaSyCuxR_sUTfFJZBDkIsauakeuqXaFxhbur4"

    .line 20
    .local v0, "apiKeyLocal":Ljava/lang/String;
    return-object v0
.end method

.method public getLocalKeyArray()[Ljava/lang/String;
    .locals 3

    .prologue
    .line 24
    const/4 v1, 0x2

    new-array v0, v1, [Ljava/lang/String;

    const/4 v1, 0x0

    const-string v2, "LIzaSyCuxR_sUTfFJZBDkIsauakeuqXaFxhbur4"

    aput-object v2, v0, v1

    const/4 v1, 0x1

    const-string v2, "MIzaSyCuxR_sUTfFJZBDkIsauakeuqXaFxhbur4"

    aput-object v2, v0, v1

    .line 25
    .local v0, "apiKeyLocalArray":[Ljava/lang/String;
    return-object v0
.end method

.method public getLocalReturnKey()Ljava/lang/String;
    .locals 1

    .prologue
    .line 29
    const-string v0, "CIzaSyCuxR_sUTfFJZBDkIsauakeuqXaFxhbur4"

    return-object v0
.end method

.method public getLocalReturnKeyArray()[Ljava/lang/String;
    .locals 3

    .prologue
    .line 33
    const/4 v0, 0x1

    new-array v0, v0, [Ljava/lang/String;

    const/4 v1, 0x0

    const-string v2, "NIzaSyCuxR_sUTfFJZBDkIsauakeuqXaFxhbur4, OIzaSyCuxR_sUTfFJZBDkIsauakeuqXaFxhbur4"

    aput-object v2, v0, v1

    return-object v0
.end method

.method public printKey()V
    .locals 2

    .prologue
    .line 45
    const-class v0, Lit/uniroma2/adidiego/apikeytestapp/JavaKey;

    invoke-virtual {v0}, Ljava/lang/Class;->getSimpleName()Ljava/lang/String;

    move-result-object v0

    const-string v1, "KIzaSyCuxR_sUTfFJZBDkIsauakeuqXaFxhbur4"

    invoke-static {v0, v1}, Landroid/util/Log;->d(Ljava/lang/String;Ljava/lang/String;)I

    .line 46
    return-void
.end method

.method public printKeyArray()V
    .locals 4

    .prologue
    .line 49
    const-class v0, Lit/uniroma2/adidiego/apikeytestapp/JavaKey;

    invoke-virtual {v0}, Ljava/lang/Class;->getSimpleName()Ljava/lang/String;

    move-result-object v0

    const/4 v1, 0x1

    new-array v1, v1, [Ljava/lang/String;

    const/4 v2, 0x0

    const-string v3, "XIzaSyCuxR_sUTfFJZBDkIsauakeuqXaFxhbur4, YIzaSyCuxR_sUTfFJZBDkIsauakeuqXaFxhbur4"

    aput-object v3, v1, v2

    invoke-static {v1}, Ljava/util/Arrays;->toString([Ljava/lang/Object;)Ljava/lang/String;

    move-result-object v1

    invoke-static {v0, v1}, Landroid/util/Log;->d(Ljava/lang/String;Ljava/lang/String;)I

    .line 50
    return-void
.end method
