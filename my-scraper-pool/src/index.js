// src/index.js

export class ScraperPool {
    constructor(state, env) {
        this.state = state;
        this.env = env;
        this.instances = [];
        this.maxInstances = 5; // Set your max instance limit here
    }

    async fetch(request) {
        let url = new URL(request.url);
        if (url.pathname === '/allocate') {
            let instance = await this.allocateInstance();
            return new Response(JSON.stringify({ instance }), { status: 200 });
        } else if (url.pathname === '/deallocate') {
            let { instance } = await request.json();
            await this.deallocateInstance(instance);
            return new Response("Deallocated", { status: 200 });
        }
        return new Response("Not found", { status: 404 });
    }

    async allocateInstance() {
        // Find an unused instance
        let unusedInstance = this.instances.find(inst => !inst.inUse);
        if (unusedInstance) {
            unusedInstance.inUse = true;
            return unusedInstance.name;
        }

        // Create a new instance if below max limit
        if (this.instances.length < this.maxInstances) {
            let instance = { name: `instance-${this.instances.length + 1}`, inUse: true };
            this.instances.push(instance);
            return instance.name;
        }

        // If all instances are in use, return an error or handle appropriately
        return "No available instances";
    }

    async deallocateInstance(instanceName) {
        let instance = this.instances.find(inst => inst.name === instanceName);
        if (instance) {
            instance.inUse = false;
        }
    }
}

export default {
    async fetch(request, env) {
        return env.SCRAPER_POOL.fetch(request);
    }
}
