import {
	createAssistantMessageEventStream,
	type Api,
	type AssistantMessageEvent,
	type AssistantMessageEventStream,
	type Context,
	type Model,
} from "@earendil-works/pi-ai";
import { builtinProviders } from "@earendil-works/pi-ai/providers/all";
import type { ExtensionAPI } from "@earendil-works/pi-coding-agent";

const PROVIDER_ID = "openai-codex-personal";
const BASE_PROVIDER_ID = "openai-codex";
const FOREIGN_WORK_HISTORY_ID = "openai-codex-work-history";

function scopeSession<T extends { sessionId?: string } | undefined>(options: T): T {
	if (!options?.sessionId) return options;
	return {
		...options,
		sessionId: `${PROVIDER_ID}:${options.sessionId}`,
	} as T;
}

function prepareContext(context: Context): Context {
	return {
		...context,
		messages: context.messages.map((message) => {
			if (message.role !== "assistant") return message;
			if (message.provider === PROVIDER_ID) return { ...message, provider: BASE_PROVIDER_ID };
			if (message.provider === BASE_PROVIDER_ID) return { ...message, provider: FOREIGN_WORK_HISTORY_ID };
			return message;
		}),
	};
}

function prepareModel(model: Model<Api>): Model<Api> {
	return { ...model, provider: BASE_PROVIDER_ID };
}

function relabelEvent(event: AssistantMessageEvent): AssistantMessageEvent {
	if ("partial" in event) {
		return { ...event, partial: { ...event.partial, provider: PROVIDER_ID } };
	}
	if (event.type === "done") {
		return { ...event, message: { ...event.message, provider: PROVIDER_ID } };
	}
	return { ...event, error: { ...event.error, provider: PROVIDER_ID } };
}

function forward(inner: AssistantMessageEventStream, model: Model<Api>): AssistantMessageEventStream {
	const outer = createAssistantMessageEventStream();

	void (async () => {
		try {
			for await (const event of inner) outer.push(relabelEvent(event));
		} catch (error) {
			outer.push({
				type: "error",
				reason: "error",
				error: {
					role: "assistant",
					content: [],
					api: model.api,
					provider: PROVIDER_ID,
					model: model.id,
					usage: {
						input: 0,
						output: 0,
						cacheRead: 0,
						cacheWrite: 0,
						totalTokens: 0,
						cost: { input: 0, output: 0, cacheRead: 0, cacheWrite: 0, total: 0 },
					},
					stopReason: "error",
					errorMessage: error instanceof Error ? error.message : String(error),
					timestamp: Date.now(),
				},
			});
		}
		outer.end();
	})();

	return outer;
}

export default function (pi: ExtensionAPI) {
	const base = builtinProviders().find((provider) => provider.id === BASE_PROVIDER_ID);
	if (!base) throw new Error("Built-in openai-codex provider was not found");

	const models = base.getModels().map((model) => ({ ...model, provider: PROVIDER_ID }));

	pi.registerProvider({
		...base,
		id: PROVIDER_ID,
		name: "OpenAI Codex (Personal)",
		getModels: () => models,
		stream: (model, context, options) =>
			forward(base.stream(prepareModel(model), prepareContext(context), scopeSession(options)), model),
		streamSimple: (model, context, options) =>
			forward(base.streamSimple(prepareModel(model), prepareContext(context), scopeSession(options)), model),
	});
}
