import { extractSecrets,
    containsValidSecret } from '../../lib/editor/text'

Meteor.methods({
    /**
      * Meteor method to execute the current model and get model instances.
      * This will call the Alloy API (webService). If the model contains
      * secrets and the previous didn't (if any), will become a new derivation
      * root (although it still registers the derivation).
      *
      * @param {String} code the Alloy model to execute
      * @param {Number} commandIndex the index of the command to execute
      * @param {String} currentModelId the id of the current model (from which
      *     the new will derive)
      *
      * @returns the instance data and the id of the new saved model
      */
    getInstances(code, commandIndex, fromPrivate, currentModelId) {
        return new Promise((resolve, reject) => {
            // if no secrets, try to extract from original
            let code_with_secrets = code
            if (currentModelId && !containsValidSecret(code) && !fromPrivate) {
                const o = Model.findOne(currentModelId).original
                code_with_secrets = code + extractSecrets(Model.findOne(o).code).secret
            }

            // save executed model to database
            const new_model = {
                time: new Date().toLocaleString(),
                // original code, without secrets
                code,
                cmd_i: commandIndex,
                derivationOf: currentModelId
            }

            // insert the new model
            const new_model_id = Model.insert(new_model)
            
            // call webservice to get instances
            HTTP.call('POST', `${Meteor.settings.env.API_URL}/getInstances`, {
                data: {
                    model: code_with_secrets,
                    numberOfInstances: Meteor.settings.env.MAX_INSTANCES,
                    commandIndex: commandIndex,
                    sessionId: new_model_id,
                    parentId: currentModelId?currentModelId:''
                }
            }, (error, result) => {
                if (error) reject(error)

                const content = JSON.parse(result.content)

                let sat
                let cmd_n
                let chk
                if (content.alloy_error) {
                    msg = content.msg
                    sat = -1
                } else {
                    // if unsat, still list with single element
                    sat = content[0].unsat ? 0 : 1
                    msg = content[0].msg
                    cmd_n = content[0].cmd_n
                    chk = content[0].check
                }
                let original
                // if the model has secrets and the previous hadn't, then it is a new root
                if (!currentModelId || fromPrivate || (containsValidSecret(code) && !containsValidSecret(Model.findOne(currentModelId).code))) {
                    original = new_model_id
                }
                // otherwise inherit the root
                else {
                    original = Model.findOne(currentModelId).original
                }

                // update the root
                Model.update({ _id: new_model_id }, { $set: { original, sat, cmd_n, cmd_c: chk, msg } })

                // resolve the promise
                resolve({
                    instances: content,
                    newModelId: new_model_id
                })
            })
        })
    }
})
