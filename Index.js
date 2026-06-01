
const { Client, GatewayIntentBits, PermissionsBitField } = require("discord.js");

const client = new Client({
    intents: [
        GatewayIntentBits.Guilds,
        GatewayIntentBits.GuildMessages,
        GatewayIntentBits.GuildMembers,
        GatewayIntentBits.MessageContent
    ]
});

const prefix = ",";

client.on("ready", () => {
    console.log(`Logged in as ${client.user.tag}`);
});

// ========== MODERATION COMMANDS ==========

client.on("messageCreate", async (message) => {
    if (message.author.bot) return;
    if (!message.content.startsWith(prefix)) return;

    const args = message.content.slice(prefix.length).trim().split(/ +/);
    const command = args.shift().toLowerCase();

    const member = message.mentions.members.first();

    // ,ping
    if (command === "ping") {
        return message.reply("Pong! 🏓");
    }

    // ,kick @user
    if (command === "kick") {
        if (!message.member.permissions.has(PermissionsBitField.Flags.KickMembers))
            return message.reply("You don't have permission!");

        if (!member) return message.reply("Mention a user!");

        await member.kick();
        message.channel.send(`👢 Kicked ${member.user.tag}`);
    }

    // ,ban @user
    if (command === "ban") {
        if (!message.member.permissions.has(PermissionsBitField.Flags.BanMembers))
            return message.reply("No permission!");

        if (!member) return message.reply("Mention a user!");

        await member.ban();
        message.channel.send(`🔨 Banned ${member.user.tag}`);
    }

    // ,mute @user (simple mute = timeout)
    if (command === "mute") {
        if (!message.member.permissions.has(PermissionsBitField.Flags.ModerateMembers))
            return message.reply("No permission!");

        if (!member) return message.reply("Mention a user!");

        await member.timeout(60 * 1000 * 10); // 10 minutes
        message.channel.send(`🔇 Muted ${member.user.tag}`);
    }

    // ,warn @user
    if (command === "warn") {
        if (!member) return message.reply("Mention a user!");

        message.channel.send(`⚠️ ${member.user.tag} has been warned.`);
    }

    // ========== ROLE COMMANDS ==========

    // ,addrole @user @role
    if (command === "addrole") {
        if (!message.member.permissions.has(PermissionsBitField.Flags.ManageRoles))
            return message.reply("No permission!");

        const role = message.mentions.roles.first();
        if (!member || !role) return message.reply("Mention user + role!");

        await member.roles.add(role);
        message.channel.send(`✅ Added role ${role.name} to ${member.user.tag}`);
    }

    // ,removerole @user @role
    if (command === "removerole") {
        if (!message.member.permissions.has(PermissionsBitField.Flags.ManageRoles))
            return message.reply("No permission!");

        const role = message.mentions.roles.first();
        if (!member || !role) return message.reply("Mention user + role!");

        await member.roles.remove(role);
        message.channel.send(`❌ Removed role ${role.name} from ${member.user.tag}`);
    }
});

client.login(process.env.TOKEN);
