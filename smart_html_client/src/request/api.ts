import request from "./request";

import {
    GenerateHtmlRequest, GenerateHtmlResponse
} from "./model"

export const generateHtml = async (requestModel: GenerateHtmlRequest): Promise<GenerateHtmlResponse> => {
    return request.post<GenerateHtmlResponse>('/session', requestModel);
};
