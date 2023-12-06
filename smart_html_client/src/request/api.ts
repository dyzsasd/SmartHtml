import request from "./request";

import {
    GenerateHtmlRequest, GenerateHtmlResponse
} from "./model"

const generateHtml = async (requestModel: GenerateHtmlRequest): Promise<GenerateHtmlResponse> => {
    return request.post<GenerateHtmlResponse>('/session', requestModel);
};
