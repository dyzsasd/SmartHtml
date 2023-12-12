import React, { useState } from "react";

import { GenerateHtmlResponse } from "../../request/model";

import { generateHtml } from "../../request/api"

import PromptInput from "../../components/PromptInput"
import HtmlIframe from "../../components/HtmlIframe"

import styles from './Main.module.scss';

const Main: React.FC = () => {
    const [viewHtml, setViewHtml] = useState<boolean>(false)
    const [loading, setLoading] = useState<boolean>(false)
    const [error, setError] = useState<boolean>(false)
    const [sessionReponse, setSessionReponse] = useState<GenerateHtmlResponse>()

    const updateRequestHtml = async (prompt: string) => {
        try{
            const result = await generateHtml({requirements: prompt})
            console.debug("updateRequestHtml => result: ", result);
            
            setSessionReponse(result)
            setLoading(false)
        }catch(e){
            console.log(e)
            setError(true)
        }
    }

    const sendPrompt = (prompt: string) => {
        console.debug("sendPrompt => prompt: ", prompt);
        setLoading(true)
        setViewHtml(true)
        setError(false)
        void updateRequestHtml(prompt)
    }

    return <div className={styles.main}>
        <HtmlIframe 
            view={viewHtml} 
            loading={loading}
            html={sessionReponse ? sessionReponse.web_pages[0].html : ""}
            css={sessionReponse ? sessionReponse.web_pages[0].css : ""}
            js={sessionReponse ? sessionReponse.web_pages[0].javascript : ""}
            error={error}
        />
        <div className={viewHtml ? `${styles['input-title-hidden']} ${styles['input-title']}` : styles['input-title']}>Let's create your dream web page</div>
        <PromptInput 
            handleEnterDown={sendPrompt}
            loading={loading}
        />
    </div>
}

export default Main;
