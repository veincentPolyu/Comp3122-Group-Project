interface Creator {
    id: number;
    name: string;
}

export interface LocationReview {
    creator: number;
    url: string;
    locationId: number;
    review: string;
    rate: number;
    updatedAt: string;
}

export interface SuggestedURL {
    creator: number;
    url: string;
    tags: string[];
    rate: number;
    locationsId: number[];
}

